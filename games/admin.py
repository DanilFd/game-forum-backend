from django.contrib import admin

# Register your models here.
from games.models import Game, Platform, Genre


@admin.register(Game)
class GamesAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'score']
    exclude = ['score']
    search_fields = ["title"]


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Genre)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ["title"]
