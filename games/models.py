from django.db import models


# Create your models here.


class Platform(models.Model):
    class Meta:
        verbose_name = "Платформа"
        verbose_name_plural = "Платформы"

    title = models.CharField(verbose_name="Платформа", max_length=20, unique=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    title = models.CharField(verbose_name='Жанр', max_length=20, unique=True)

    def __str__(self):
        return self.title.lower()


class Game(models.Model):
    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ['-id']

    img = models.ImageField(verbose_name="Изображение")
    title = models.CharField(verbose_name="Название", max_length=50, unique=True)
    platforms = models.ManyToManyField(Platform, verbose_name="Платформы")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    release_date = models.DateField(verbose_name="Дата выхода")
    score = models.FloatField(verbose_name="Оценка", default=0)

    def __str__(self):
        return self.title
