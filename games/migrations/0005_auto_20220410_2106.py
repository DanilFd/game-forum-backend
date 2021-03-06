# Generated by Django 3.2.7 on 2022-04-10 18:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_alter_usergamerelation_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='score',
        ),
        migrations.AlterField(
            model_name='game',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3, validators=[django.core.validators.MaxValueValidator(10)], verbose_name='Рейтинг'),
        ),
    ]
