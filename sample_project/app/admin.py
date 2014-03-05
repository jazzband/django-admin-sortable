from django.contrib import admin

from adminsortable.admin import (SortableAdmin, SortableTabularInline,
    SortableStackedInline, SortableGenericStackedInline)
from adminsortable.utils import get_is_sortable
from app.models import (Category, Widget, Project, Credit, Note, GenericNote,
    Component, Person)


admin.site.register(Category, SortableAdmin)


class ComponentInline(SortableStackedInline):
    model = Component

    def queryset(self, request):
        qs = super(ComponentInline, self).queryset(
            request).exclude(title__icontains='2')
        if get_is_sortable(qs):
            self.model.is_sortable = True
        else:
            self.model.is_sortable = False
        return qs


class WidgetAdmin(SortableAdmin):
    def queryset(self, request):
        """
        A simple example demonstrating that adminsortable works even in
        situations where you need to filter the queryset in admin. Here,
        we are just filtering out `widget` instances with an pk higher
        than 3
        """
        qs = super(WidgetAdmin, self).queryset(request)
        return qs.filter(id__lte=3)

    inlines = [ComponentInline]

admin.site.register(Widget, WidgetAdmin)


class CreditInline(SortableTabularInline):
    model = Credit


class NoteInline(SortableStackedInline):
    model = Note
    extra = 0


class GenericNoteInline(SortableGenericStackedInline):
    model = GenericNote
    extra = 0


class ProjectAdmin(SortableAdmin):
    inlines = [CreditInline, NoteInline, GenericNoteInline]
    list_display = ['__unicode__', 'category']

admin.site.register(Project, ProjectAdmin)


class PersonAdmin(SortableAdmin):
    list_display = ['__unicode__', 'is_board_member']

admin.site.register(Person, PersonAdmin)
