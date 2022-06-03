from django.contrib import admin

# Register your models here.
from blogs.models import Blog


@admin.register(Blog)
class BlogsAdmin(admin.ModelAdmin):
    exclude = ["views_count"]
    list_display = ["title", 'views_count', 'creation_date']
    search_fields = ["title"]
    sortable_by = ['views_count', 'creation_date']
    readonly_fields = ['creator', 'img', 'rating']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
