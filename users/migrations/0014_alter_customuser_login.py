# Generated by Django 3.2.7 on 2022-05-01 17:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_useraction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='login',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(5)], verbose_name='Логин'),
        ),
    ]