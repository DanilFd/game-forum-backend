# Generated by Django 3.2.7 on 2022-05-19 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0009_bloguserrelation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloguserrelation',
            old_name='game',
            new_name='blog',
        ),
    ]