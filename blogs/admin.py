from django.contrib import admin

# Register your models here.
from blogs.models import Blog


@admin.register(Blog)
class BlogsAdmin(admin.ModelAdmin):
    exclude = ["views_count"]
    list_display = ["title", 'views_count', 'creation_date']
    search_fields = ["title"]
    sortable_by = ['views_count', 'creation_date']
    readonly_fields = ['creator']

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)
