from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from django.conf import settings

from comments.models import NewsCommentComplaint, NewsComment, BlogCommentComplaint, BlogComment


@admin.register(NewsCommentComplaint)
class NewsCommentComplaintAdmin(admin.ModelAdmin):
    readonly_fields = ['comment', 'reason', 'show_news_url', 'time_add', 'description']

    def show_news_url(self, obj: NewsCommentComplaint):
        comment_url = "http://" + settings.FRONTEND_URL + "/news/all/" + str(obj.comment.news_item.id)
        return format_html("<a href='{url}'>{url}</a>", url=comment_url)

    show_news_url.short_description = "Ссылка на новость:"


@admin.register(BlogCommentComplaint)
class NewsCommentComplaintAdmin(admin.ModelAdmin):
    readonly_fields = ['comment', 'reason', 'show_news_url', 'time_add', 'description']

    def show_news_url(self, obj: BlogCommentComplaint):
        comment_url = "http://" + settings.FRONTEND_URL + "/news/all/" + str(obj.comment.blog_item.id)
        return format_html("<a href='{url}'>{url}</a>", url=comment_url)

    show_news_url.short_description = "Ссылка на блог:"


@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    readonly_fields = ['id']


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
