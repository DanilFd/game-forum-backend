from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.
from users.models import CustomUser


class Blog(models.Model):
    class Meta:
        ordering = ['creation_date']

    img = models.ImageField(verbose_name="Изображение")
    title = models.CharField(verbose_name="Название", max_length=50, unique=True)
    creation_date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    creator = models.ForeignKey(CustomUser, verbose_name="Создатель", on_delete=models.CASCADE, blank=True)
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    views_count = models.IntegerField(verbose_name="Количество просмотров", default=0)
    content = models.TextField(verbose_name="Контент")

    def __str__(self):
        return self.title


