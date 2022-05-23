from django import forms
from django.contrib import admin

from games.models import UserGameRelation
from news.models import NewsItem, NewsCategory


class CategoryInLine(admin.TabularInline):
    model = NewsCategory
    extra = 1
    show_change_link = True


@admin.register(NewsItem)
class NewsAdmin(admin.ModelAdmin):
    exclude = ["views_count"]
    list_display = ["title", 'views_count', 'creation_date']
    search_fields = ["title"]
    sortable_by = ['views_count', 'creation_date']
    readonly_fields = ['creator']

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


@admin.register(NewsCategory)
class CategoryNewsAdmin(admin.ModelAdmin):
    list_display = ["title"]
    exclude = ["slug"]


