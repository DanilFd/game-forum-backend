from django import forms
from django.contrib import admin

# Register your models here.
from news.models import NewsItem
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = NewsItem
        fields = '__all__'


@admin.register(NewsItem)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    readonly_fields = ["views_count"]
