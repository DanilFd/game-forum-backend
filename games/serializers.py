from rest_framework import serializers

from games.models import Game, Platform, Genre, UserGameRelation
from games.utils.convert_month_to_str import convert_month_to_str


class ListPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', "title", 'slug']


class ListGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', "title", 'slug']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'platforms', 'genres', 'release_date', 'score', 'img', 'is_following']

    platforms = ListPlatformSerializer(many=True)
    genres = ListGenreSerializer(many=True)
    release_date = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    def get_release_date(self, obj: Game):
        month = convert_month_to_str(obj.release_date.month)
        return f"{obj.release_date.day} {month} {obj.release_date.year} г."

    def get_is_following(self, obj: Game):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        relation = UserGameRelation.objects.filter(game=obj, user=user).first()
        if relation is None:
            return False
        return relation.is_following


class UserGameRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGameRelation
        fields = ['is_following']
