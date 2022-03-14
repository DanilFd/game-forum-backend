from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from comments.models import NewsCommentComplaint, NewsComment, UserCommentRelation
from django.conf import settings


@admin.register(NewsCommentComplaint)
class NewsCommentComplaintAdmin(admin.ModelAdmin):
    readonly_fields = ['comment', 'reason', 'show_news_url', 'time_add', 'description']

    def show_news_url(self, obj: NewsCommentComplaint):
        comment_url = "http://" + settings.FRONTEND_URL + "/news/all/" + str(obj.comment.news_item.id)
        return format_html("<a href='{url}'>{url}</a>", url=comment_url)

    show_news_url.short_description = "Ссылка на новость:"


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
