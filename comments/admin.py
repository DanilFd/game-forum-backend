from django.contrib import admin

# Register your models here.
from comments.models import NewsCommentComplaint


@admin.register(NewsCommentComplaint)
class NewsCommentComplaintAdmin(admin.ModelAdmin):
    readonly_fields = ['comment', 'reason', 'time_add']
