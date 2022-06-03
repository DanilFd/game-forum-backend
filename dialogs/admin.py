from django.contrib import admin

# Register your models here.
from dialogs.models import DialogMessage, Dialog


@admin.register(DialogMessage)
class CategoryNewsAdmin(admin.ModelAdmin):
    readonly_fields = ['sender', 'dialog', 'content', 'sending_date']

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Dialog)
class CategoryNewsAdmin(admin.ModelAdmin):
    exclude = ['user_that_deleted']
    readonly_fields = ['title', 'owner', 'responder', 'creation_date']

    def has_add_permission(self, request, obj=None):
        return False
