# Generated by Django 3.2.7 on 2021-12-22 08:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('profile_img', models.ImageField(default='defaultProfileImg.png', upload_to='', verbose_name='Изображение профиля')),
                ('login', models.CharField(max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(6)], verbose_name='Логин')),
                ('email', models.EmailField(max_length=35, unique=True, verbose_name='Email')),
                ('gender', models.CharField(choices=[('Male', 'Женский'), ('Female', 'Мужской'), ('Not specified', 'Не указан')], default='Не указан', max_length=15, verbose_name='Пол')),
                ('birthday_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('discord', models.CharField(blank=True, max_length=30, null=True, verbose_name='Discord')),
                ('role', models.CharField(choices=[('User', 'User'), ('Moderator', 'Moderator'), ('Editor', 'Editor'), ('Admin', 'Admin')], default='User', max_length=15, verbose_name='Роль')),
                ('last_visit', models.DateTimeField(auto_now_add=True, verbose_name='Последнее посещение')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Последняя дата захода')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('is_active', models.BooleanField(default=False, help_text='Определяет, следует ли считать этого пользователя активным. Снимите этот флажок вместо удаления учетных записей.', verbose_name='Active')),
                ('is_staff', models.BooleanField(default=False, help_text='Определяет, может ли пользователь войти на этот сайт администратора.', verbose_name='Staff status')),
                ('is_superuser', models.BooleanField(default=False, help_text='Указывает, что у этого пользователя есть все разрешения без их явного назначения.', verbose_name='Superuser status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователя',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]