from rest_framework import serializers

from games.models import Game
from games.serializers import GameSerializer
from news.models import NewsItem, NewsCategory
from news.replace_content import replace_content
from users.serializers import UserProfileSerializer, ModestUserProfileSerializer


class NewsItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["id", "title", "slug"]


class ListNewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ["id", "title", "image", "creation_date", "categories"]

    categories = NewsItemCategorySerializer(many=True)


class DetailNewsItemSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        return replace_content(obj.content)

    games = GameSerializer(read_only=True, many=True)

    class Meta:
        model = NewsItem
        fields = ["id", "title", "content", "views_count", "creation_date", "games", "creator"]

    creator = ModestUserProfileSerializer()


class ListNewsCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["title", "slug", "id"]
