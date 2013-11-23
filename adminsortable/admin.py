import json

from django import VERSION as DJANGO_VERSION
from django.contrib.contenttypes.generic import (GenericStackedInline,
    GenericTabularInline)

DJANGO_MINOR_VERSION = DJANGO_VERSION[1]

from django.conf import settings

if DJANGO_MINOR_VERSION < 5:
    from django.conf.urls.defaults import patterns, url
else:
    from django.conf.urls import patterns, url

from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import capfirst

from adminsortable.utils import get_is_sortable
from adminsortable.fields import SortableForeignKey
from adminsortable.models import Sortable

STATIC_URL = settings.STATIC_URL


class SortableAdminBase(object):
    def changelist_view(self, request, extra_context=None):
        """
        If the model that inherits Sortable has more than one object,
        its sort order can be changed. This view adds a link to the
        object_tools block to take people to the view to change the sorting.
        """

        if get_is_sortable(self.queryset(request)):
            self.change_list_template = \
                self.sortable_change_list_with_sort_link_template
            self.is_sortable = True

        if extra_context is None:
            extra_context = {}

        extra_context.update({
            'change_list_template_extends': self.change_list_template_extends
        })
        return super(SortableAdminBase, self).changelist_view(request,
            extra_context=extra_context)


class SortableAdmin(SortableAdminBase, ModelAdmin):
    """
    Admin class to add template overrides and context objects to enable
    drag-and-drop ordering.
    """
    ordering = ('order', 'id')

    sortable_change_list_with_sort_link_template = \
        'adminsortable/change_list_with_sort_link.html'
    sortable_change_form_template = 'adminsortable/change_form.html'
    sortable_change_list_template = 'adminsortable/change_list.html'
    sortable_javascript_includes_template = \
        'adminsortable/shared/javascript_includes.html'

    change_form_template_extends = 'admin/change_form.html'
    change_list_template_extends = 'admin/change_list.html'

    class Meta:
        abstract = True

    def _get_sortable_foreign_key(self):
        sortable_foreign_key = None
        for field in self.model._meta.fields:
            if isinstance(field, SortableForeignKey):
                sortable_foreign_key = field
                break
        return sortable_foreign_key

    def get_urls(self):
        urls = super(SortableAdmin, self).get_urls()
        admin_urls = patterns('',

            # this view changes the order
            url(r'^sorting/do-sorting/(?P<model_type_id>\d+)/$',
                self.admin_site.admin_view(self.do_sorting_view),
                name='admin_do_sorting'),

            # this view shows a link to the drag-and-drop view
            url(r'^sort/$', self.admin_site.admin_view(self.sort_view),
                name='admin_sort'),
        )
        return admin_urls + urls

    def sort_view(self, request):
        """
        Custom admin view that displays the objects as a list whose sort
        order can be changed via drag-and-drop.
        """
        opts = self.model._meta
        has_perm = request.user.has_perm('{0}.{1}'.format(opts.app_label,
            opts.get_change_permission()))

        objects = self.queryset(request)

        # Determine if we need to regroup objects relative to a
        # foreign key specified on the model class that is extending Sortable.
        # Legacy support for 'sortable_by' defined as a model property
        sortable_by_property = getattr(self.model, 'sortable_by', None)

        # `sortable_by` defined as a SortableForeignKey
        sortable_by_fk = self._get_sortable_foreign_key()
        sortable_by_class_is_sortable = get_is_sortable(objects)

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
            sortable_by_class_display_name = sortable_by_fk.rel.to \
                ._meta.verbose_name_plural
            sortable_by_class = sortable_by_fk.rel.to
            sortable_by_expression = sortable_by_fk.name.lower()

        else:
            # model is not sortable by another model
            sortable_by_class = sortable_by_expression = \
                sortable_by_class_display_name = \
                sortable_by_class_is_sortable = None

        if sortable_by_property or sortable_by_fk:
            # Order the objects by the property they are sortable by,
            # then by the order, otherwise the regroup
            # template tag will not show the objects correctly
            objects = objects.order_by(sortable_by_expression, 'order')

        try:
            verbose_name_plural = opts.verbose_name_plural.__unicode__()
        except AttributeError:
            verbose_name_plural = opts.verbose_name_plural

        context = {
            'title': u'Drag and drop {0} to change display order'.format(
                capfirst(verbose_name_plural)),
            'opts': opts,
            'app_label': opts.app_label,
            'has_perm': has_perm,
            'objects': objects,
            'group_expression': sortable_by_expression,
            'sortable_by_class': sortable_by_class,
            'sortable_by_class_is_sortable': sortable_by_class_is_sortable,
            'sortable_by_class_display_name': sortable_by_class_display_name,
            'sortable_javascript_includes_template':
            self.sortable_javascript_includes_template
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

    def change_view(self, request, object_id, extra_context=None):
        self.has_sortable_tabular_inlines = False
        self.has_sortable_stacked_inlines = False

        if extra_context is None:
            extra_context = {}

        extra_context.update({
            'change_form_template_extends': self.change_form_template_extends
        })

        for klass in self.inlines:
            if issubclass(klass, SortableTabularInline):
                self.has_sortable_tabular_inlines = True
            if issubclass(klass, SortableStackedInline):
                self.has_sortable_stacked_inlines = True

        if self.has_sortable_tabular_inlines or \
                self.has_sortable_stacked_inlines:

            self.change_form_template = self.sortable_change_form_template

            extra_context.update({
                'sortable_javascript_includes_template':
                self.sortable_javascript_includes_template,
                'has_sortable_tabular_inlines':
                self.has_sortable_tabular_inlines,
                'has_sortable_stacked_inlines':
                self.has_sortable_stacked_inlines
            })

        return super(SortableAdmin, self).change_view(request, object_id,
            extra_context=extra_context)

    def do_sorting_view(self, request, model_type_id=None):
        """
        This view sets the ordering of the objects for the model type
        and primary keys passed in. It must be an Ajax POST.
        """
        response = {'objects_sorted': False}

        if request.is_ajax() and request.method == 'POST':
            try:
                indexes = list(map(str, request.POST.get('indexes', []).split(',')))
                klass = ContentType.objects.get(id=model_type_id).model_class()
                objects_dict = dict([(str(obj.pk), obj) for obj in
                    klass.objects.filter(pk__in=indexes)])
                if '-order' in klass._meta.ordering:  # desc order
                    start_object = max(objects_dict.values(),
                        key=lambda x: getattr(x, 'order'))
                    start_index = getattr(start_object, 'order') \
                        or len(indexes)
                    step = -1
                else:  # 'order' is default, asc order
                    start_object = min(objects_dict.values(),
                        key=lambda x: getattr(x, 'order'))
                    start_index = getattr(start_object, 'order') or 0
                    step = 1

                for index in indexes:
                    obj = objects_dict.get(index)
                    setattr(obj, 'order', start_index)
                    obj.save()
                    start_index += step
                response = {'objects_sorted': True}
            except (KeyError, IndexError, klass.DoesNotExist, AttributeError, ValueError):
                pass

        return HttpResponse(json.dumps(response, ensure_ascii=False),
            content_type='application/json')


class SortableInlineBase(SortableAdminBase, InlineModelAdmin):
    def __init__(self, *args, **kwargs):
        super(SortableInlineBase, self).__init__(*args, **kwargs)

        if not issubclass(self.model, Sortable):
            raise Warning(u'Models that are specified in SortableTabluarInline'
                ' and SortableStackedInline must inherit from Sortable')

    def queryset(self, request):
        qs = super(SortableInlineBase, self).queryset(request)
        if get_is_sortable(qs):
            self.model.is_sortable = True
        else:
            self.model.is_sortable = False
        return qs


class SortableTabularInline(TabularInline, SortableInlineBase):
    """Custom template that enables sorting for tabular inlines"""
    template = 'adminsortable/edit_inline/tabular.html'


class SortableStackedInline(StackedInline, SortableInlineBase):
    """Custom template that enables sorting for stacked inlines"""
    template = 'adminsortable/edit_inline/stacked.html'


class SortableGenericTabularInline(GenericTabularInline, SortableInlineBase):
    """Custom template that enables sorting for tabular inlines"""
    template = 'adminsortable/edit_inline/tabular.html'


class SortableGenericStackedInline(GenericStackedInline, SortableInlineBase):
    """Custom template that enables sorting for stacked inlines"""
    template = 'adminsortable/edit_inline/stacked.html'
