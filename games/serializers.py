from rest_framework import serializers

from games.models import Game, Platform, Genre


class GamePlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ["title"]


class GameGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["title"]


class ListGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['title', 'platform', 'genre', 'release_date', 'score']

    platform = GamePlatformSerializer(many=True)
    genre = GameGenreSerializer(many=True)
