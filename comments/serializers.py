from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable, NotFound

from comments.models import NewsComment, NewsCommentComplaint
from comments.serializer_fields import RecursiveField
from dialogs.models import Dialog, DialogMessage, UnreadMessage
from users.models import CustomUser
from users.serializers import ModestUserProfileSerializer


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsComment
        fields = ['id', 'creator', 'creation_date', 'content', 'parent', 'children', "news_item"]
        extra_kwargs = {
            'news_item': {'write_only': True}
        }

    creator = ModestUserProfileSerializer(read_only=True)
    children = RecursiveField(many=True, read_only=True)

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class ListNewsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsComment
        fields = ['id', 'creator', 'creation_date', 'content', 'children']

    children = RecursiveField(many=True)
    creator = ModestUserProfileSerializer(read_only=True)
    creation_date = serializers.DateTimeField(format="%d.%m.%Y, %H:%M", read_only=True)


class CreateComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCommentComplaint
        fields = ['comment', 'reason', 'time_add']

    time_add = serializers.DateTimeField(format="%d.%m.%Y, %H:%M", read_only=True)
