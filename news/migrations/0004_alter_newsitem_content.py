# Generated by Django 3.2.7 on 2021-11-28 16:44

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_newsitem_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsitem',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Контент'),
        ),
    ]
