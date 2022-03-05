from datetime import date, timedelta

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser, UserUserRelation
from users.utils import get_web_url


class CustomTokeObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        request = self.context['request']
        web_url = get_web_url(request)
        token = super().get_token(user)
        token['login'] = user.login
        token['role'] = user.role
        token['profile_img'] = web_url + user.profile_img.url
        print("url:", user.profile_img.url)
        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        request = self.context['request']
        web_url = get_web_url(request)
        refresh = RefreshToken(attrs['refresh'])
        access_token = refresh.access_token
        access_token['profile_img'] = web_url + CustomUser.objects.get(id=access_token['user_id']).profile_img.url
        data = {'access': str(access_token)}
        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)
        return data


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
        fields = ['birthday_date', 'gender', 'discord', 'about_custom_user', 'profile_img']


class ModestUserProfileSerializer(UserProfileSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_img', 'login', 'date_joined', 'gender', 'age']


class ModestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'profile_img', 'login']


class RateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUserRelation
        fields = ['rate']

    def update(self, instance: UserUserRelation, validated_data):
        initial_rate = instance.rate
        instance.rate = validated_data['rate']
        instance.save()
        if initial_rate == 'Like':
            if instance.rate == 'Dislike':
                instance.user1.rating -= 2
                instance.user1.save()
            elif instance.rate is None:
                instance.user1.rating -= 1
                instance.user1.save()
        elif initial_rate == 'Dislike':
            if instance.rate == 'Like':
                instance.user1.rating += 2
                instance.user1.save()
            elif instance.rate is None:
                instance.user1.rating += 1
                instance.user1.save()
        elif initial_rate is None:
            if instance.rate == 'Like':
                instance.user1.rating += 1
                instance.user1.save()
            elif instance.rate == 'Dislike':
                instance.user1.rating -= 1
                instance.user1.save()

        return instance
