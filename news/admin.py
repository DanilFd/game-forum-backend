from django.contrib import admin

# Register your models here.
from news.models import NewsItem


@admin.register(NewsItem)
class NewsAdmin(admin.ModelAdmin):
    readonly_fields = ["views_count"]
