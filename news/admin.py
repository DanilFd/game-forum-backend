from django import forms
from django.contrib import admin

from news.models import NewsItem, NewsCategory
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = NewsItem
        fields = '__all__'


@admin.register(NewsItem)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    exclude = ["views_count"]
    list_display = ["title"]
    search_fields = ["title"]


@admin.register(NewsCategory)
class CategoryNewsAdmin(admin.ModelAdmin):
    list_display = ["title"]
    exclude = ["slug"]


