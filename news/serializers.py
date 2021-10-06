from rest_framework import serializers

from news.models import NewsItem, NewsCategory
from news.replace_content import replace_content


class ListNewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ["id", "title", "image", "creation_date", "categories"]


class DetailNewsItemSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        return replace_content(obj.content)

    class Meta:
        model = NewsItem
        fields = ["id", "title", "content", "views_count", "creation_date"]


class ListNewsCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ["title", "slug", "id"]
