# Generated by Django 3.2.7 on 2021-12-14 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20211204_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=35, unique=True, verbose_name='email'),
        ),
    ]