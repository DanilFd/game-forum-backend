# Generated by Django 3.2.7 on 2021-11-28 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211128_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('User', 'User'), ('Moderator', 'Moderator'), ('Editor', 'Editor'), ('Admin', 'Admin')], default='User', max_length=15, verbose_name='Роль'),
        ),
    ]
