from rest_framework import serializers

from games.models import Game, Platform, Genre
from games.utils.convert_month_to_str import convert_month_to_str


class ListPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', "title"]


class ListGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', "title"]


class ListGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'platforms', 'genres', 'release_date', 'score', 'img']

    platforms = ListPlatformSerializer(many=True)
    genres = ListGenreSerializer(many=True)
    release_date = serializers.SerializerMethodField()

    def get_release_date(self, obj: Game):
        month = convert_month_to_str(obj.release_date.month)
        return f"{obj.release_date.day} {month} {obj.release_date.year} г."
