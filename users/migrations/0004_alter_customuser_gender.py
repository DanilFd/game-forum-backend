# Generated by Django 3.2.7 on 2021-12-22 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('Мужской', 'Мужской'), ('Женский', 'Женский'), ('Не указан', 'Не указан')], default='Not specified', max_length=15, verbose_name='Пол'),
        ),
    ]
