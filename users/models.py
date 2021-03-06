from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, login, password=None):
        if not email:
            raise ValueError('Email is required')
        if not login:
            raise ValueError('Login is required')
        user = self.model(
            email=self.normalize_email(email),
            login=login,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, login, password=None):

        user = self.create_user(
            email=email,
            login=login,
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.role = 'Admin'
        user.save(using=self._db)
        return user


ROLE_CHOICES = (
    ('User', 'User'),
    ('Moderator', 'Moderator'),
    ('Editor', 'Editor'),
    ('Admin', 'Admin')

)

GENDER_CHOICES = (
    ('Мужской', 'Мужской'),
    ('Женский', 'Женский'),
    ('Не указан', 'Не указан')
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    profile_img = models.ImageField(verbose_name="Изображение профиля", default="defaultProfileImg.png")
    login = models.CharField(verbose_name="Логин", max_length=20, unique=True, validators=[MinLengthValidator(5)])
    email = models.EmailField(verbose_name="Email", max_length=35, unique=True)
    gender = models.CharField(verbose_name="Пол", choices=GENDER_CHOICES, max_length=15, default='Не указан')
    birthday_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    discord = models.CharField(verbose_name="Discord", max_length=30, null=True, blank=True)
    about_custom_user = models.TextField(verbose_name="Коротко о себе", null=True, blank=True)
    role = models.CharField(verbose_name="Роль", choices=ROLE_CHOICES, max_length=15, default='User')
    last_visit = models.DateTimeField('Последнее посещение', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Последняя дата захода", auto_now=True)
    date_joined = models.DateTimeField(verbose_name="Дата регистрации", auto_now_add=True)
    is_active = models.BooleanField(default=False, verbose_name="Active",
                                    help_text='Определяет, следует ли считать этого пользователя активным. '
                                              'Снимите этот флажок вместо удаления учетных записей.')
    is_staff = models.BooleanField(default=False, verbose_name="Staff status",
                                   help_text='Определяет, может ли пользователь войти на этот сайт администратора.')
    is_superuser = models.BooleanField(default=False, verbose_name="Superuser status",
                                       help_text='Указывает, что у этого пользователя есть все '
                                                 'разрешения без их явного назначения.')
    rating = models.DecimalField(default=0, decimal_places=2, max_digits=6, verbose_name='Рейтинг')

    USERNAME_FIELD = 'login'

    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.login


RATE_CHOICES = (
    ('Like', 'Like'),
    ('Dislike', 'Dislike')
)


class UserUserRelation(models.Model):
    class Meta:
        pass

    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="liked_me")
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="my_likes")
    rate = models.TextField(choices=RATE_CHOICES, default=None, blank=True, null=True)


ACTION_CHOICES = (
    ("send_message", "send_message"),
    ("rate_user", "rate_user"),
)


class UserAction(models.Model):
    class Meta:
        pass

    action_type = models.TextField(choices=ACTION_CHOICES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    moment = models.DateTimeField(auto_now_add=True)
