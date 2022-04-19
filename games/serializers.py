from django.db.models import Avg
from rest_framework import serializers

from games.lists_serializers import ListPlatformSerializer, ListGenreSerializer
from games.models import Game, UserGameRelation
from games.utils.convert_month_to_str import convert_month_to_str
from news.serializers import DetailNewsItemSerializer


class GameDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'platforms', 'genres', 'release_date', 'img', 'is_following', 'slug',
                  'rating', 'screenshots', 'developer', 'user_rating', 'rating_of_other_users', 'news']

    platforms = ListPlatformSerializer(many=True)
    genres = ListGenreSerializer(many=True)
    release_date = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    screenshots = serializers.SlugRelatedField(many=True, read_only=True, slug_field="image_url")
    user_rating = serializers.SerializerMethodField()
    rating_of_other_users = serializers.SerializerMethodField()
    news = DetailNewsItemSerializer(many=True, read_only=True)

    def get_rating_of_other_users(self, obj: Game):
        user = self.context['request'].user

        if user.is_authenticated:
            others_rates = UserGameRelation.objects.exclude(user=user).filter(game=obj)
        else:
            others_rates = UserGameRelation.objects.filter(game=obj)
        return dict(
            users_count=others_rates.count(),
            users_rating=others_rates.aggregate(Avg('rate'))['rate__avg'] or 0
        )

    def get_user_rating(self, obj: Game):
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0
        user_relation = UserGameRelation.objects.filter(game=obj, user=user).first()
        if not user_relation:
            return None
        return user_relation.rate

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
        fields = ['is_following', 'rate', 'game_rating']

    game_rating = serializers.SerializerMethodField()

    def get_game_rating(self, obj: UserGameRelation):
        return obj.game.rating

    def update(self, instance: UserGameRelation, validated_data):
        initial_rate = validated_data
        updated_relation: UserGameRelation = super().update(instance, validated_data)
        if initial_rate != updated_relation:
            updated_relation.game.rating = updated_relation.game.user_relations.aggregate(Avg('rate'))['rate__avg'] or 0
            updated_relation.game.save()
        return updated_relation
