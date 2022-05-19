from django.db import models

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


class NewsComment(models.Model):
    class Meta:
        ordering = ['creation_date']

    news_item = models.ForeignKey(NewsItem, verbose_name="Новость", on_delete=models.CASCADE, related_name="comments")
    creator = models.ForeignKey(CustomUser, verbose_name='Создатель', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)
    content = models.TextField(verbose_name="Контент", max_length=100)
    parent = models.ForeignKey('NewsComment', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_deleted = models.BooleanField(verbose_name="Удален ли", default=False)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class NewsCommentComplaint(models.Model):
    class Meta:
        verbose_name = "Жалобу"
        verbose_name_plural = "Жалобы"

    comment = models.ForeignKey(NewsComment, on_delete=models.CASCADE, verbose_name="Комментарий")
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, verbose_name="Причина")
    time_add = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки жалобы.")
    description = models.TextField(max_length=70, verbose_name="Описание жалобы", null=True, blank=True)

    def __str__(self):
        return self.comment.content


RATE_CHOICES = (
    ('Like', 'Like'),
    ('Dislike', 'Dislike')
)


class UserCommentRelation(models.Model):
    class Meta:
        pass

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(NewsComment, on_delete=models.CASCADE)
    rate = models.TextField(choices=RATE_CHOICES, default=None, blank=True, null=True)
