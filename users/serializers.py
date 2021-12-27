from datetime import date, timedelta

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import CustomUser
from users.utils import get_web_url


class CustomTokeObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        request = self.context['request']
        web_url = get_web_url(request)
        token = super().get_token(user)
        token['login'] = user.login
        token['role'] = user.role
        token['profile_img'] = web_url + user.profile_img.url
        return token


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_img', 'login', 'date_joined', 'last_visit', 'birthday_date', 'discord', 'gender',
                  'about_custom_user', 'age', 'email']

    age = SerializerMethodField()
    birthday_date = serializers.DateField(format='%d.%m.%Y')

    def get_age(self, instance: CustomUser):
        if instance.birthday_date is None:
            return None
        return (date.today() - instance.birthday_date) // timedelta(days=365.2425)


class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['birthday_date', 'gender', 'discord', 'about_custom_user']
