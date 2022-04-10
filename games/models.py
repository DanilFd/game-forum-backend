from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models, IntegrityError
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from users.models import CustomUser


class Platform(models.Model):
    class Meta:
        verbose_name = "Платформа"
        verbose_name_plural = "Платформы"

    title = models.CharField(verbose_name="Платформа", max_length=20, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        translated = self.title.translate(
            str.maketrans(
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"
            ))
        self.slug = slugify(translated)
        try:
            super(Platform, self).save(*args, **kwargs)

        except IntegrityError as err:
            print(err.message)
            if 'UNIQUE constraint' in err.message:
                raise ValidationError({
                    'Платформа': 'Платформа уже существует.'
                })

    def __str__(self):
        return self.title


class Genre(models.Model):
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    title = models.CharField(verbose_name='Жанр', max_length=20, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        translated = self.title.translate(
            str.maketrans(
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"
            ))
        self.slug = slugify(translated)
        try:
            super(Genre, self).save(*args, **kwargs)

        except IntegrityError as err:
            print(err.message)
            if 'UNIQUE constraint' in err.message:
                raise ValidationError({
                    'Платформа': 'Платформа уже существует.'
                })

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
    slug = models.SlugField(unique=True)
    rating = models.DecimalField(default=0, decimal_places=1, max_digits=3, validators=[MaxValueValidator(10)],
                                 verbose_name="Рейтинг")

    def save(self, *args, **kwargs):
        translated = self.title.translate(
            str.maketrans(
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"
            ))
        self.slug = slugify(translated)
        try:
            super(Game, self).save(*args, **kwargs)

        except IntegrityError as err:
            if 'UNIQUE constraint' in err.message:
                raise ValidationError({
                    'Категория': 'Категория уже существует.'
                })

    def __str__(self):
        return self.title


class UserGameRelation(models.Model):
    class Meta:
        verbose_name = "Избранная игра"
        verbose_name_plural = "Избранные игры"

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="user_relations")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_following = models.BooleanField(default=False)
    rate = models.DecimalField(default=None, null=True, decimal_places=1, max_digits=3,
                               validators=[MaxValueValidator(10)])


class GameImage(models.Model):
    class Meta:
        verbose_name = "Скриншот"
        verbose_name_plural = "Скриншоты игры"

    image = models.ImageField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="screenshots")

    @property
    def image_url(self):
        return f"http://{settings.BACKEND_URL}{self.image.url}"
