from rest_framework import serializers

from news.models import NewsItem, NewsCategory


class CreateNewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = "__all__"


class ListNewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ["id", "title", "image", "creation_date", "category"]


class CreateCategoryNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = "__all__"
