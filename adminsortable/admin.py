import json

from django import VERSION

from django.conf import settings

try:
    from django.conf.urls import url
except ImportError:
    # Django < 1.4
    from django.conf.urls.defaults import url

from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.contrib.admin.options import InlineModelAdmin

try:
    from django.contrib.contenttypes.admin import (GenericStackedInline,
                                                   GenericTabularInline)
except:
    # Django < 1.7
    from django.contrib.contenttypes.generic import (GenericStackedInline,
                                                     GenericTabularInline)

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import capfirst
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from adminsortable.fields import SortableForeignKey
from adminsortable.models import SortableMixin
from adminsortable.utils import get_is_sortable

STATIC_URL = settings.STATIC_URL


class SortableAdminBase(object):
    sortable_change_list_with_sort_link_template = \
        'adminsortable/change_list_with_sort_link.html'
    sortable_change_form_template = 'adminsortable/change_form.html'
    sortable_change_list_template = 'adminsortable/change_list.html'

    change_form_template_extends = 'admin/change_form.html'
    change_list_template_extends = 'admin/change_list.html'

    def changelist_view(self, request, extra_context=None):
        """
        If the model that inherits Sortable has more than one object,
        its sort order can be changed. This view adds a link to the
        object_tools block to take people to the view to change the sorting.
        """

        try:
            qs_method = getattr(self, 'get_queryset', self.queryset)
        except AttributeError:
            qs_method = self.get_queryset

        if get_is_sortable(qs_method(request)):
            self.change_list_template = \
                self.sortable_change_list_with_sort_link_template
            self.is_sortable = True

        if extra_context is None:
            extra_context = {}

        extra_context.update({
            'change_list_template_extends': self.change_list_template_extends,
            'sorting_filters': [sort_filter[0] for sort_filter
                in getattr(self.model, 'sorting_filters', [])]
        })
        return super(SortableAdminBase, self).changelist_view(request,
            extra_context=extra_context)


class SortableAdmin(SortableAdminBase, ModelAdmin):
    """
    Admin class to add template overrides and context objects to enable
    drag-and-drop ordering.
    """

    class Meta:
        abstract = True

    @property
    def has_sortable_tabular_inlines(self):
        base_classes = (SortableTabularInline, SortableGenericTabularInline)
        return any(issubclass(klass, base_classes) for klass in self.inlines)

    @property
    def has_sortable_stacked_inlines(self):
        base_classes = (SortableStackedInline, SortableGenericStackedInline)
        return any(issubclass(klass, base_classes) for klass in self.inlines)

    @property
    def change_form_template(self):
        if self.has_sortable_tabular_inlines or self.has_sortable_stacked_inlines:
            return self.sortable_change_form_template
        return super(SortableAdmin, self).change_form_template

    def get_urls(self):
        urls = super(SortableAdmin, self).get_urls()
        opts = self.model._meta
        try:
            info = opts.app_label, opts.model_name
        except AttributeError:
            # Django < 1.7
            info = opts.app_label, opts.modul_name

        # this ajax view changes the order of instances of self.model
        admin_do_sorting_url = url(
            r'^sort/do-sorting/$',
            self.admin_site.admin_view(self.do_sorting_view),
            name='%s_%s_do_sorting' % info)

        # this ajax view changes the order of instances of inline models
        admin_do_inline_sorting_url = url(
            r'^sort/do-sorting/(?P<model_type_id>\d+)/$',
            self.admin_site.admin_view(self.do_sorting_view),
            name='%s_%s_do_sorting' % info)

        # this view displays the sortable objects
        admin_sort_url = url(
            r'^sort/$',
            self.admin_site.admin_view(self.sort_view),
            name='%s_%s_sort' % info)

        urls = [
            admin_do_inline_sorting_url,
            admin_do_sorting_url,
            admin_sort_url
        ] + urls
        return urls

    def sort_view(self, request):
        """
        Custom admin view that displays the objects as a list whose sort
        order can be changed via drag-and-drop.
        """
        if not self.has_change_permission(request):
            raise PermissionDenied

        opts = self.model._meta

        jquery_lib_path = 'admin/js/jquery.js' if VERSION < (1, 9) \
            else 'admin/js/vendor/jquery/jquery.js'

        # get sort group index from querystring if present
        sort_filter_index = request.GET.get('sort_filter')

        filters = {}
        if sort_filter_index:
            try:
                filters = self.model.sorting_filters[int(sort_filter_index)][1]
            except (IndexError, ValueError):
                pass

        # Apply any sort filters to create a subset of sortable objects
        try:
            qs_method = getattr(self, 'get_queryset', self.queryset)
        except AttributeError:
            qs_method = self.get_queryset
        objects = qs_method(request).filter(**filters)

        # Determine if we need to regroup objects relative to a
        # foreign key specified on the model class that is extending Sortable.
        # Legacy support for 'sortable_by' defined as a model property
        sortable_by_property = getattr(self.model, 'sortable_by', None)

        # see if our model is sortable by a SortableForeignKey field
        # and that the number of objects available is >= 2
        sortable_by_fk = None
        sortable_by_field_name = None
        sortable_by_class_is_sortable = False

        for field in self.model._meta.fields:
            if isinstance(field, SortableForeignKey):
                sortable_by_fk = field.rel.to
                sortable_by_field_name = field.name.lower()
                sortable_by_class_is_sortable = sortable_by_fk.objects.count() >= 2

        if sortable_by_property:
            # backwards compatibility for < 1.1.1, where sortable_by was a
            # classmethod instead of a property
            try:
                sortable_by_class, sortable_by_expression = \
                    sortable_by_property()
            except (TypeError, ValueError):
                sortable_by_class = self.model.sortable_by
                sortable_by_expression = sortable_by_class.__name__.lower()

            sortable_by_class_display_name = sortable_by_class._meta \
                .verbose_name_plural

        elif sortable_by_fk:
            # get sortable by properties from the SortableForeignKey
            # field - supported in 1.3+
            sortable_by_class_display_name = sortable_by_fk._meta.verbose_name_plural
            sortable_by_class = sortable_by_fk
            sortable_by_expression = sortable_by_field_name

        else:
            # model is not sortable by another model
            sortable_by_class = sortable_by_expression = \
                sortable_by_class_display_name = \
                sortable_by_class_is_sortable = None

        if sortable_by_property or sortable_by_fk:
            # Order the objects by the property they are sortable by,
            # then by the order, otherwise the regroup
            # template tag will not show the objects correctly

            try:
                order_field_name = opts.model._meta.ordering[0]
            except (AttributeError, IndexError):
                # for Django 1.5.x
                order_field_name = opts.ordering[0]
            except (AttributeError, IndexError):
                order_field_name = 'order'

            objects = objects.order_by(sortable_by_expression, order_field_name)

        try:
            verbose_name_plural = opts.verbose_name_plural.__unicode__()
        except AttributeError:
            verbose_name_plural = opts.verbose_name_plural

        context = {
            'title': u'Drag and drop {0} to change display order'.format(
                capfirst(verbose_name_plural)),
            'opts': opts,
            'app_label': opts.app_label,
            'has_perm': True,
            'objects': objects,
            'group_expression': sortable_by_expression,
            'sortable_by_class': sortable_by_class,
            'sortable_by_class_is_sortable': sortable_by_class_is_sortable,
            'sortable_by_class_display_name': sortable_by_class_display_name,
            'jquery_lib_path': jquery_lib_path,
            'csrf_cookie_name': getattr(settings, 'CSRF_COOKIE_NAME', 'csrftoken')
        }
        return render(request, self.sortable_change_list_template, context)

    def add_view(self, request, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}

        extra_context.update({
            'change_form_template_extends': self.change_form_template_extends
        })
        return super(SortableAdmin, self).add_view(request, form_url,
            extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        if extra_context is None:
            extra_context = {}

        extra_context.update({
            'change_form_template_extends': self.change_form_template_extends,
            'has_sortable_tabular_inlines': self.has_sortable_tabular_inlines,
            'has_sortable_stacked_inlines': self.has_sortable_stacked_inlines,
            'csrf_cookie_name': getattr(settings, 'CSRF_COOKIE_NAME', 'csrftoken')
        })

        return super(SortableAdmin, self).change_view(request, object_id,
            form_url='', extra_context=extra_context)

    @method_decorator(require_POST)
    def do_sorting_view(self, request, model_type_id=None):
        """
        This view sets the ordering of the objects for the model type
        and primary keys passed in. It must be an Ajax POST.
        """
        if not self.has_change_permission(request):
            raise PermissionDenied

        response = {'objects_sorted': False}

        if request.is_ajax():
            try:
                if model_type_id is None:
                    klass = self.model
                else:
                    klass = get_object_or_404(ContentType,
                                              id=model_type_id).model_class()
                    if klass not in (inline.model for inline in self.inlines):
                        raise Http404(
                            'There is no inline model with type id: {0}'.format(
                                model_type_id))

                indexes = list(map(str,
                    request.POST.get('indexes', []).split(',')))
                objects_dict = dict([(str(obj.pk), obj) for obj in
                    klass.objects.filter(pk__in=indexes)])

                order_field_name = klass._meta.ordering[0]

                if order_field_name.startswith('-'):
                    order_field_name = order_field_name[1:]
                    step = -1
                    start_object = max(objects_dict.values(),
                        key=lambda x: getattr(x, order_field_name))
                else:
                    step = 1
                    start_object = min(objects_dict.values(),
                        key=lambda x: getattr(x, order_field_name))

                start_index = getattr(start_object, order_field_name,
                    len(indexes))

                for index in indexes:
                    obj = objects_dict.get(index)
                    setattr(obj, order_field_name, start_index)
                    obj.save()
                    start_index += step
                response = {'objects_sorted': True}
            except (KeyError, IndexError, klass.DoesNotExist,
                    AttributeError, ValueError):
                pass

        return HttpResponse(json.dumps(response, ensure_ascii=False),
            content_type='application/json')


class NonSortableParentAdmin(SortableAdmin):
    def changelist_view(self, request, extra_context=None):
        return super(SortableAdminBase, self).changelist_view(request,
            extra_context=extra_context)


class SortableInlineBase(SortableAdminBase, InlineModelAdmin):
    def __init__(self, *args, **kwargs):
        super(SortableInlineBase, self).__init__(*args, **kwargs)

        if not issubclass(self.model, SortableMixin):
            raise Warning(u'Models that are specified in SortableTabularInline'
                ' and SortableStackedInline must inherit from SortableMixin'
                ' (or Sortable for legacy implementations)')

    def get_queryset(self, request):
        if VERSION < (1, 6):
            qs = super(SortableInlineBase, self).queryset(request)
        else:
            qs = super(SortableInlineBase, self).get_queryset(request)

        if get_is_sortable(qs):
            self.model.is_sortable = True
        else:
            self.model.is_sortable = False
        return qs

    if VERSION < (1, 6):
        queryset = get_queryset


class SortableTabularInline(TabularInline, SortableInlineBase):
    """Custom template that enables sorting for tabular inlines"""
    if VERSION >= (1, 10):
        template = 'adminsortable/edit_inline/tabular-1.10.x.html'
    elif VERSION < (1, 6):
        template = 'adminsortable/edit_inline/tabular-1.5.x.html'
    else:
        template = 'adminsortable/edit_inline/tabular.html'


class SortableStackedInline(StackedInline, SortableInlineBase):
    """Custom template that enables sorting for stacked inlines"""
    if VERSION >= (1, 10):
        template = 'adminsortable/edit_inline/stacked-1.10.x.html'
    elif VERSION < (1, 6):
        template = 'adminsortable/edit_inline/stacked-1.5.x.html'
    else:
        template = 'adminsortable/edit_inline/stacked.html'


class SortableGenericTabularInline(GenericTabularInline, SortableInlineBase):
    """Custom template that enables sorting for tabular inlines"""
    if VERSION >= (1, 10):
        template = 'adminsortable/edit_inline/tabular-1.10.x.html'
    elif VERSION < (1, 6):
        template = 'adminsortable/edit_inline/tabular-1.5.x.html'
    else:
        template = 'adminsortable/edit_inline/tabular.html'


class SortableGenericStackedInline(GenericStackedInline, SortableInlineBase):
    """Custom template that enables sorting for stacked inlines"""
    if VERSION >= (1, 10):
        template = 'adminsortable/edit_inline/stacked-1.10.x.html'
    elif VERSION < (1, 6):
        template = 'adminsortable/edit_inline/stacked-1.5.x.html'
    else:
        template = 'adminsortable/edit_inline/stacked.html'
