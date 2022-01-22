from django.contrib import admin

# Register your models here.
from dialogs.models import DialogMessage, Dialog, UnreadMessage


@admin.register(DialogMessage)
class CategoryNewsAdmin(admin.ModelAdmin):
    list_display = ['content', 'sender', 'sending_date']


@admin.register(Dialog)
class CategoryNewsAdmin(admin.ModelAdmin):
    list_display = ["title", 'id']


@admin.register(UnreadMessage)
class TestAdmin(admin.ModelAdmin):
    list_display = ["user", "message"]
