# Generated by Django 3.2.7 on 2021-12-22 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20211222_1642'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='about_user',
            new_name='about_custom_user',
        ),
    ]
