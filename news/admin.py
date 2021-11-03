from django import forms
from django.contrib import admin

from news.models import NewsItem, NewsCategory
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CategoryInLine(admin.TabularInline):
    model = NewsCategory
    extra = 1
    show_change_link = True


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())


@admin.register(NewsItem)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    exclude = ["views_count"]
    list_display = ["title", 'views_count', 'creation_date']
    search_fields = ["title"]
    sortable_by = ['views_count', 'creation_date']


@admin.register(NewsCategory)
class CategoryNewsAdmin(admin.ModelAdmin):
    list_display = ["title"]
    exclude = ["slug"]
