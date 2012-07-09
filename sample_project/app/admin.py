from django.contrib import admin

from adminsortable.admin import SortableAdmin, SortableTabularInline, SortableStackedInline
from app.models import Category, Project, Credit, Note


admin.site.register(Category, SortableAdmin)


class CreditInline(SortableTabularInline):
    model = Credit


class NoteInline(SortableStackedInline):
    model = Note
    extra = 0


class ProjectAdmin(SortableAdmin):
    inlines = [CreditInline, NoteInline]
    list_display = ['__unicode__', 'category']

admin.site.register(Project, ProjectAdmin)
