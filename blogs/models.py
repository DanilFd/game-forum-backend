from django.core.validators import MaxValueValidator, MinLengthValidator
from django.db import models

# Create your models here.
from users.models import CustomUser


class Blog(models.Model):
    class Meta:
        ordering = ['-creation_date']
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"

    img = models.ImageField(verbose_name="Изображение")
    title = models.CharField(verbose_name="Название", max_length=100, validators=[MinLengthValidator(5)], unique=True)
    creation_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    creator = models.ForeignKey(CustomUser, verbose_name="Создатель", on_delete=models.CASCADE, blank=True)
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    views_count = models.IntegerField(verbose_name="Количество просмотров", default=0)
    content = models.TextField(verbose_name="Контент")

    def __str__(self):
        return self.title


class ContentImage(models.Model):
    class Meta:
        pass

    image = models.ImageField()


RATE_CHOICES = (
    ('Like', 'Like'),
    ('Dislike', 'Dislike')
)


class BlogUserRelation(models.Model):
    class Meta:
        pass

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="user_relations")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rate = models.TextField(choices=RATE_CHOICES, default=None, blank=True, null=True)
