from datetime import date, timedelta

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from comments.models import NewsComment
from users.models import CustomUser, UserUserRelation, UserAction
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
                  'about_custom_user', 'age', 'email', 'rate', 'rating']

    rate = SerializerMethodField()
    age = SerializerMethodField()
    birthday_date = serializers.DateField(format='%d.%m.%Y')

    def get_age(self, instance: CustomUser):
        if instance.birthday_date is None:
            return None
        return (date.today() - instance.birthday_date) // timedelta(days=365.2425)

    def get_rate(self, obj: CustomUser):
        if not self.context['request'].user.is_authenticated:
            return None
        found_rate = UserUserRelation.objects.filter(user1=obj, user2=self.context['request'].user).first()
        if found_rate is None:
            return None
        return found_rate.rate


class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['birthday_date', 'gender', 'discord', 'about_custom_user', 'profile_img']


class ModestUserProfileSerializer(UserProfileSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_img', 'login', 'date_joined', 'gender', 'age', 'rating', 'comments_count']

    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj: CustomUser):
        return NewsComment.objects.filter(creator=obj).count()


class ModestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'profile_img', 'login']


class RateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUserRelation
        fields = ['rate', 'rating']
        read_only_fields = ['rating']

    rating = serializers.SerializerMethodField()

    def get_rating(self, obj: UserUserRelation):
        return obj.user1.rating

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
        UserAction.objects.create(action_type="rate_user", user=instance.user2)
        return instance


class RegistrationByGoogleSerializer(serializers.ModelSerializer):
    login = serializers.CharField(min_length=1, max_length=25)

    class Meta:
        model = CustomUser
        fields = ['login', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(login=validated_data['login'], email=validated_data['email'],
                                              password=validated_data['password'])
        user.is_active = True
        user.save()
        return user


class ModestUserForSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'login', 'rating', 'date_joined', 'profile_img', 'comments_count']

    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj: CustomUser):
        return NewsComment.objects.filter(creator=obj).count()
