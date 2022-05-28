import datetime
from datetime import timedelta, date

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from blogs.models import Blog
from comments.models import NewsComment, BlogComment
from games.models import Game
from users.models import CustomUser, UserUserRelation


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'profile_img', 'login', 'date_joined', 'last_visit', 'birthday_date', 'discord', 'gender',
                  'about_custom_user', 'age', 'email', 'rate', 'rating', 'comments_count', 'blogs_count', 'games_count']

    rate = SerializerMethodField()
    age = SerializerMethodField()
    birthday_date = serializers.DateField(format='%d.%m.%Y')
    comments_count = serializers.SerializerMethodField()
    blogs_count = serializers.SerializerMethodField()
    games_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj: CustomUser):
        return NewsComment.objects.filter(creator=obj).count() + BlogComment.objects.filter(creator=obj).count()

    def get_blogs_count(self, obj: CustomUser):
        return Blog.objects.filter(creator=obj).count()

    def get_games_count(self, obj: CustomUser):
        return dict(favorite_games_count=Game.objects.filter(user_relations__user=obj,
                                                             user_relations__is_following=True).count(),
                    rated_games_count=Game.objects.filter(
                        user_relations__user=obj).exclude(user_relations__rate__isnull=True).count())

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
