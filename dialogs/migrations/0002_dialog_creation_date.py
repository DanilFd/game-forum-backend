# Generated by Django 3.2.7 on 2022-01-06 16:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialog',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 1, 6, 19, 7, 37, 576860)),
            preserve_default=False,
        ),
    ]