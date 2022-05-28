from rest_framework import serializers

from comments.models import NewsComment
from games.game_serializer import ListGameSerializer, ModestGameSerializer
from news.models import NewsItem, NewsCategory
from news.replace_content import replace_content
from users.serializers import ModestUserProfileSerializer


class NewsItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["id", "title", "slug"]


class ListNewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ["id", "title", "image", "creation_date", "categories", "comments_count"]

    categories = NewsItemCategorySerializer(many=True)
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj: NewsItem):
        return NewsComment.objects.filter(news_item_id=obj.id).count()


class DetailNewsItemSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        return replace_content(obj.content)

    class Meta:
        model = NewsItem
        fields = ["id", "title", "content", "views_count", "creation_date", "games", "creator", "comments_count"]

    games = ListGameSerializer(read_only=True, many=True)

    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj: NewsItem):
        return NewsComment.objects.filter(news_item_id=obj.id).count()

    creator = ModestUserProfileSerializer()


class ListNewsCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["title", "slug", "id"]


class FavoritesNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ["id", "title", "image", "creation_date", "games"]

    games = ModestGameSerializer(many=True)


class ModestNewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ['id', "title", "image", "creation_date"]

    creation_date = serializers.DateTimeField(format="%d.%m.%Y, %H:%M", read_only=True)


class NewsSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ['id', 'title', 'is_news_comment']

    is_news_comment = serializers.SerializerMethodField()

    def get_is_news_comment(self, obj):
        return True
