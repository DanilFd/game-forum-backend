# Generated by Django 3.2.7 on 2021-12-18 06:36

from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, unique=True, verbose_name='Заголовок')),
                ('slug', models.SlugField(unique=True, verbose_name='Путь')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=130, verbose_name='Заголовок')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Контент')),
                ('views_count', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('categories', models.ManyToManyField(to='news.NewsCategory', verbose_name='Категории')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.game', verbose_name='Игра')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['-creation_date'],
            },
        ),
    ]
