from django.db import models, IntegrityError

from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from rest_framework.exceptions import ValidationError

from games.models import Game
from users.models import CustomUser


class NewsCategory(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Заголовок", max_length=25, unique=True)
    slug = models.SlugField(verbose_name="Путь", unique=True)

    def save(self, *args, **kwargs):
        translated = self.title.translate(
            str.maketrans(
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"
            ))
        self.slug = slugify(translated)
        try:
            super(NewsCategory, self).save(*args, **kwargs)

        except IntegrityError as err:
            print(err.message)
            if 'UNIQUE constraint' in err.message:
                raise ValidationError({
                    'Категория': 'Категория уже существует.'
                })

    def __str__(self):
        return self.title


class NewsItem(models.Model):
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-creation_date']

    title = models.CharField(verbose_name="Заголовок", max_length=130)
    image = models.ImageField(verbose_name="Изображение")
    content = CKEditor5Field(verbose_name="Контент", config_name='extends')
    views_count = models.IntegerField(verbose_name="Количество просмотров", default=0)
    creation_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    categories = models.ManyToManyField(NewsCategory, verbose_name="Категории")
    games = models.ManyToManyField(Game, verbose_name="Игра", blank=True, related_name="news")
    creator = models.ForeignKey(CustomUser, verbose_name="Создатель", on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title
