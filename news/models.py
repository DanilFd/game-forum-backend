from django.db import models

# Create your models here.
from django.utils.text import slugify


class NewsCategory(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Заголовок", max_length=25)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        translated = self.title.translate(
            str.maketrans(
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"
            ))
        self.slug = slugify(translated)
        super(NewsCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class NewsItem(models.Model):
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    title = models.CharField(verbose_name="Заголовок", max_length=130)
    image = models.ImageField(verbose_name="Изображение")
    content = models.TextField(verbose_name="Контент")
    views_count = models.IntegerField(verbose_name="Количество просмотров", default=0)
    creation_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, verbose_name="Категория", related_name="test")

    def __str__(self):
        return self.title
