from django.contrib import admin

from adminsortable.admin import (SortableAdmin, SortableTabularInline,
    SortableStackedInline, SortableGenericStackedInline,
    NonSortableParentAdmin)
from adminsortable.utils import get_is_sortable
from .models import (Category, Widget, Project, Credit, Note, GenericNote,
    Component, Person, NonSortableCategory, SortableCategoryWidget,
    SortableNonInlineCategory, NonSortableCredit, NonSortableNote,
    CustomWidget, CustomWidgetComponent, BackwardCompatibleWidget)


admin.site.register(Category, SortableAdmin)


class ComponentInline(SortableStackedInline):
    # fieldsets = (
    #     ('foo', {
    #         'classes': ('collapse',),
    #         'fields': ('title',)
    #     }),
    #     ('', {
    #         'classes': ('collapse',),
    #         'fields': ('widget',)
    #     }),
    # )
    model = Component

    def get_queryset(self, request):
        qs = super(ComponentInline, self).get_queryset(
            request).exclude(title__icontains='2')
        if get_is_sortable(qs):
            self.model.is_sortable = True
        else:
            self.model.is_sortable = False
        return qs


class WidgetAdmin(SortableAdmin):
    def get_queryset(self, request):
        """
        A simple example demonstrating that adminsortable works even in
        situations where you need to filter the queryset in admin. Here,
        we are just filtering out `widget` instances with an pk higher
        than 3
        """
        qs = super(WidgetAdmin, self).get_queryset(request)
        return qs.filter(id__lte=3)

    inlines = [ComponentInline]

admin.site.register(Widget, WidgetAdmin)


class CreditAdmin(SortableAdmin):
    raw_id_fields = ('project',)

admin.site.register(Credit, CreditAdmin)


class CreditInline(SortableTabularInline):
    model = Credit
    extra = 1


class NoteInline(SortableStackedInline):
    model = Note
    extra = 2

    def after_sorting(self):
        print('I happened after sorting')


class GenericNoteInline(SortableGenericStackedInline):
    model = GenericNote
    extra = 0


class NonSortableCreditInline(admin.TabularInline):
    model = NonSortableCredit
    extra = 1


class NonSortableNoteInline(admin.StackedInline):
    model = NonSortableNote
    extra = 0


class ProjectAdmin(SortableAdmin):
    inlines = [
        CreditInline, NoteInline, GenericNoteInline,
        NonSortableCreditInline, NonSortableNoteInline
    ]
    list_display = ['__str__', 'category', 'isApproved',]
    list_filter = ('category__title', 'isApproved',)
    after_sorting_js_callback_name = 'afterSortCallback'
    search_fields = ['title']
    sortable_change_list_template = 'adminsortable/custom_change_list.html'
    sortable_change_form_template = 'adminsortable/custom_change_form.html'

    def after_sorting(self):
        print('I happened after sorting')

admin.site.register(Project, ProjectAdmin)


class PersonAdmin(SortableAdmin):
    list_display = ['__str__', 'is_board_member']

admin.site.register(Person, PersonAdmin)


class SortableCategoryWidgetInline(SortableStackedInline):
    model = SortableCategoryWidget
    extra = 0


class NonSortableCategoryAdmin(NonSortableParentAdmin):
    inlines = [SortableCategoryWidgetInline]

admin.site.register(NonSortableCategory, NonSortableCategoryAdmin)


class CustomWidgetComponentInline(SortableStackedInline):
    model = CustomWidgetComponent
    extra = 0


class CustomWidgetAdmin(SortableAdmin):
    inlines = [CustomWidgetComponentInline]


admin.site.register(SortableNonInlineCategory, SortableAdmin)
admin.site.register(CustomWidget, CustomWidgetAdmin)
admin.site.register(BackwardCompatibleWidget, SortableAdmin)
