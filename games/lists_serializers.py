from rest_framework import serializers

from games.models import Platform, Genre


class ListPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', "title", 'slug']


class ListGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', "title", 'slug']
