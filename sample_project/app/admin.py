from django.contrib import admin

from adminsortable.admin import SortableAdmin, SortableTabularInline
from app.models import Category, Project, Credit


admin.site.register(Category, SortableAdmin)


class CreditInline(SortableTabularInline):
    model = Credit


class ProjectAdmin(SortableAdmin):
    inlines = [CreditInline]
    list_display = ['__unicode__', 'category']

admin.site.register(Project, ProjectAdmin)
