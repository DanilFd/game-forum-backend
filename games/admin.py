from django.contrib import admin

# Register your models here.
from games.models import Game, Platform, Genre, UserGameRelation, GameImage


class ImageInline(admin.StackedInline):
    model = GameImage


@admin.register(Game)
class GamesAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'rating', 'developer']
    exclude = ['slug']
    search_fields = ["title"]
    readonly_fields = ['rating']
    inlines = [
        ImageInline
    ]


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ["title"]
    exclude = ['slug']


@admin.register(Genre)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ["title"]
    exclude = ['slug']


@admin.register(UserGameRelation)
class UserGameRelationAdmin(admin.ModelAdmin):
    list_display = ['game', 'user', 'is_following','rate']

