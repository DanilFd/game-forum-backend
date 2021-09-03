from django.db import models


# Create your models here.


class NewsItem(models.Model):
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    title = models.CharField(verbose_name="Заголовок", max_length=130)
    image = models.ImageField(verbose_name="Изображение")
    content = models.TextField(verbose_name="Контент")
    views_count = models.IntegerField(verbose_name="Количество просмотров", default=0)
    creation_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
