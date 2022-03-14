import decimal
from rest_framework import serializers
from comments.models import NewsComment, NewsCommentComplaint, UserCommentRelation
from comments.serializer_fields import RecursiveField
from users.serializers import ModestUserProfileSerializer
from decimal import Decimal


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsComment
        fields = ['id', 'creator', 'creation_date', 'content', 'parent', 'children', "news_item", 'is_owner']
        extra_kwargs = {
            'news_item': {'write_only': True}
        }

    is_owner = serializers.SerializerMethodField()
    creator = ModestUserProfileSerializer(read_only=True)
    children = RecursiveField(many=True, read_only=True)

    def get_is_owner(self, obj):
        return self.context['request'].user.id == obj.creator.id

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class ListNewsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsComment
        fields = ['id', 'creator', 'creation_date', 'content', 'is_owner', 'is_deleted', 'parent', 'rating']

    is_owner = serializers.SerializerMethodField()
    children = RecursiveField(many=True)
    creator = ModestUserProfileSerializer(read_only=True)
    creation_date = serializers.DateTimeField(format="%d.%m.%Y, %H:%M", read_only=True)

    def get_is_owner(self, obj: NewsComment):
        return self.context['request'].user.id == obj.creator.id


class CreateComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCommentComplaint
        fields = ['comment', 'reason', 'time_add', 'description']

    time_add = serializers.DateTimeField(format="%d.%m.%Y, %H:%M", read_only=True)


class RateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCommentRelation
        fields = ['rate', 'rating']
        read_only_fields = ['rating']

    rating = serializers.SerializerMethodField()

    def get_rating(self, obj: UserCommentRelation):
        return obj.comment.rating

    def update(self, instance: UserCommentRelation, validated_data):
        initial_rate = instance.rate
        instance.rate = validated_data['rate']
        instance.save()
        if initial_rate == 'Like':
            if instance.rate == 'Dislike':
                instance.user.rating -= Decimal(0.20)
                instance.comment.rating -= 2

            elif instance.rate is None:
                instance.user.rating -= Decimal(0.10)
                instance.comment.rating -= 1

        elif initial_rate == 'Dislike':
            if instance.rate == 'Like':
                instance.user.rating += Decimal(0.20)
                instance.comment.rating += 2

            elif instance.rate is None:
                instance.user.rating += Decimal(0.10)
                instance.comment.rating += 1

        elif initial_rate is None:
            if instance.rate == 'Like':
                instance.user.rating += Decimal(0.10)
                instance.comment.rating += 1

            elif instance.rate == 'Dislike':
                instance.user.rating -= Decimal(0.10)
                instance.comment.rating -= 1

        instance.comment.save()
        instance.user.save()
        return instance
