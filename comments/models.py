from django.db import models

from blogs.models import Blog
from news.models import NewsItem
from users.models import CustomUser

REASON_CHOICES = (
    ('Контент для взрослых', 'Контент для взрослых'),
    ('Мультиаккаунт', 'Мультиаккаунт'),
    ('Оскорбление', 'Оскорбление'),
    ('Реклама', 'Реклама'),
    ('Спам', 'Спам'),
    ('Другое', 'Другое'),
)
RATE_CHOICES = (
    ('Like', 'Like'),
    ('Dislike', 'Dislike')
)


class AbstractComment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['creation_date']
        abstract = True

    creation_date = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)
    content = models.TextField(verbose_name="Контент", max_length=100)
    is_deleted = models.BooleanField(verbose_name="Удален ли", default=False)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class NewsComment(AbstractComment):
    class Meta(AbstractComment.Meta):
        verbose_name = 'Комментарий новости'
        verbose_name_plural = 'Комментарии новостей'

    creator = models.ForeignKey(CustomUser, verbose_name='Создатель', on_delete=models.CASCADE)
    news_item = models.ForeignKey(NewsItem, verbose_name="Новость", on_delete=models.CASCADE,
                                  related_name="news_comments")
    parent = models.ForeignKey('NewsComment', on_delete=models.CASCADE, null=True, blank=True, related_name="children")


class BlogComment(AbstractComment):
    class Meta(AbstractComment.Meta):
        verbose_name = 'Комментарий блога'
        verbose_name_plural = 'Комментарии блогов'

    creator = models.ForeignKey(CustomUser, verbose_name='Создатель', on_delete=models.CASCADE)
    blog_item = models.ForeignKey(Blog, verbose_name='Блог', on_delete=models.CASCADE, related_name="blog_comments")
    parent = models.ForeignKey('BlogComment', on_delete=models.CASCADE, null=True, blank=True, related_name="children")


class AbstractCommentComplain(models.Model):
    class Meta:
        verbose_name = "Жалобу"
        verbose_name_plural = "Жалобы"
        abstract = True

    reason = models.CharField(max_length=20, choices=REASON_CHOICES, verbose_name="Причина")
    time_add = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки жалобы.")
    description = models.TextField(max_length=70, verbose_name="Описание жалобы", null=True, blank=True)


class NewsCommentComplaint(AbstractCommentComplain):
    class Meta(AbstractCommentComplain.Meta):
        verbose_name = "Жалобу"
        verbose_name_plural = "Жалобы"

    comment = models.ForeignKey(NewsComment, on_delete=models.CASCADE, verbose_name="Комментарий")

    def __str__(self):
        return self.comment.content


class BlogCommentComplaint(AbstractCommentComplain):
    class Meta(AbstractCommentComplain.Meta):
        verbose_name = "Жалобу"
        verbose_name_plural = "Жалобы"

    comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE, verbose_name="Комментарий")

    def __str__(self):
        return self.comment.content


class AbstractUserCommentRelation(models.Model):
    class Meta:
        abstract = True

    rate = models.TextField(choices=RATE_CHOICES, default=None, blank=True, null=True)


class UserNewsCommentRelation(AbstractUserCommentRelation):
    class Meta(AbstractUserCommentRelation.Meta):
        pass

    comment = models.ForeignKey(NewsComment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class UserBlogCommentRelation(AbstractUserCommentRelation):
    class Meta(AbstractUserCommentRelation.Meta):
        pass

    comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
