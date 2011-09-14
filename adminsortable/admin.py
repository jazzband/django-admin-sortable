import json
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import capfirst
from django.views.decorators.csrf import csrf_exempt

from adminsortable.models import Sortable

STATIC_URL = settings.STATIC_URL


class SortableAdmin(ModelAdmin):
    ordering = ('order', 'id')

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(SortableAdmin, self).__init__(*args, **kwargs)
        self.has_sortable_tabular_inlines = False
        self.has_sortable_stacked_inlines = False
        for klass in self.inlines:
            if issubclass(klass, SortableTabularInline):
                if klass.model.is_sortable():
                    self.has_sortable_tabular_inlines = True
            if issubclass(klass, SortableStackedInline):
                if klass.model.is_sortable():
                    self.has_sortable_stacked_inlines = True

    def get_urls(self):
        urls = super(SortableAdmin, self).get_urls()
        admin_urls = patterns('',
            url(r'^sorting/do-sorting/(?P<model_type_id>\d+)/$',
                self.admin_site.admin_view(self.do_sorting_view),
                name='admin_do_sorting'), #this view changes the order
            url(r'^sort/$', self.admin_site.admin_view(self.sort_view),
                name='admin_sort'), #this view shows a link to the drag-and-drop view
        )
        return admin_urls + urls

    def sort_view(self, request):
        """
        Custom admin view that displays the objects as a list whose sort order can be
        changed via drag-and-drop.
        """
        opts = self.model._meta
        admin_site = self.admin_site
        has_perm = request.user.has_perm(opts.app_label + '.' + opts.get_change_permission())
        objects = self.model.objects.all()

        """
        Determine if we need to regroup objects relative to a foreign key specified on the
        model class that is extending Sortable.
        """
        sortable_by = getattr(self.model, 'sortable_by', None)
        if sortable_by:
            sortable_by_class, sortable_by_expression = sortable_by()
            sortable_by_class_display_name = sortable_by_class._meta.verbose_name_plural
            sortable_by_class_is_sortable = sortable_by_class.is_sortable()
        else:
            sortable_by_class = sortable_by_expression = sortable_by_class_display_name = \
                sortable_by_class_is_sortable = None

        try:
            verbose_name_plural = opts.verbose_name_plural.__unicode__()
        except AttributeError:
            verbose_name_plural = opts.verbose_name_plural

        context = {
            'title' : 'Drag and drop %s to change display order' % capfirst(verbose_name_plural),
            'opts' : opts,
            'root_path' : '/%s' % admin_site.root_path,
            'app_label' : opts.app_label,
            'has_perm' : has_perm,
            'objects' : objects,
            'group_expression' : sortable_by_expression,
            'sortable_by_class' : sortable_by_class,
            'sortable_by_class_is_sortable' : sortable_by_class_is_sortable,
            'sortable_by_class_display_name' : sortable_by_class_display_name
        }
        return render(request, 'adminsortable/change_list.html', context)

    def changelist_view(self, request, extra_context=None):
        """
        If the model that inherits Sortable has more than one object,
        its sort order can be changed. This view adds a link to the object_tools
        block to take people to the view to change the sorting.
        """
        if self.model.is_sortable():
            self.change_list_template = 'adminsortable/change_list_with_sort_link.html'
        return super(SortableAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, extra_context=None):
        if self.has_sortable_tabular_inlines or self.has_sortable_stacked_inlines:
            self.change_form_template = 'adminsortable/change_form.html'
            extra_context = {
                'has_sortable_tabular_inlines' : self.has_sortable_tabular_inlines,
                'has_sortable_stacked_inlines' : self.has_sortable_stacked_inlines
            }
        return super(SortableAdmin, self).change_view(request, object_id, extra_context=extra_context)

    @csrf_exempt
    def do_sorting_view(self, request, model_type_id=None):
        """
        This view sets the ordering of the objects for the model type and primary keys
        passed in. It must be an Ajax POST.
        """

        if request.is_ajax() and request.method == 'POST':
            klass = ContentType.objects.get(id=model_type_id).model_class()
            for order, pk in enumerate(request.POST['indexes'].split(',')):
                obj = klass.objects.get(pk=pk)
                obj.order = order
                obj.save()
            response = {'objects_sorted' : True}
        else:
            response = {'objects_sorted' : False}
        return HttpResponse(json.dumps(response, ensure_ascii=False),
                            mimetype='application/json')


class SortableInlineBase(InlineModelAdmin):
    def __init__(self, *args, **kwargs):
        super(SortableInlineBase, self).__init__(*args, **kwargs)

        if not issubclass(self.model, Sortable):
            raise Warning(u'Models that are specified in SortableTabluarInline and SortableStackedInline must inherit from Sortable')

        self.is_sortable = self.model.is_sortable()


class SortableTabularInline(SortableInlineBase, TabularInline):
    """Custom template that enables sorting for tabular inlines"""
    template = 'adminsortable/edit_inline/tabular.html'


class SortableStackedInline(SortableInlineBase, StackedInline):
    """Custom template that enables sorting for stacked inlines"""
    template = 'adminsortable/edit_inline/stacked.html'
