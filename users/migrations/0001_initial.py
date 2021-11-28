# Generated by Django 3.2.7 on 2021-11-28 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('login', models.CharField(max_length=20, unique=True, verbose_name='Логин')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Последняя дата захода')),
                ('role', models.CharField(max_length=15, verbose_name='Роль')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
