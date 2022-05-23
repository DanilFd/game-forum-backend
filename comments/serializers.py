from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable

from blogs.serializers import BlogSourceSerializer
from comments.models import NewsComment, NewsCommentComplaint, UserNewsCommentRelation, BlogComment, \
    UserBlogCommentRelation, BlogCommentComplaint
from comments.serializer_fields import RecursiveField
from news.serializers import NewsSourceSerializer
from users.models import UserAction
from decimal import Decimal

from users.serializers import ModestUserProfileSerializer

create_comment_fields = ['id', 'creator', 'creation_date', 'content', 'parent', 'children', 'is_owner', 'rating']
list_comment_fields = ['id', 'creator', 'creation_date', 'content', 'is_owner', 'is_deleted', 'parent', 'rating',
                       'rate', 'source']

create_comment_complaint_fields = ['comment', 'reason', 'time_add', 'description']


class CreateCommentSerializerMixin(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    creator = ModestUserProfileSerializer(read_only=True)
    children = RecursiveField(many=True, read_only=True)

    def get_is_owner(self, obj):
        return self.context['request'].user.id == obj.creator.id

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class ListCommentSerializerMixin(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    creator = ModestUserProfileSerializer(read_only=True)
    creation_date = serializers.DateTimeField(format="%d.%m.%Y, %H:%M", read_only=True)
    rate = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        return self.context['request'].user.id == obj.creator.id


class CreateNewsCommentSerializer(CreateCommentSerializerMixin):
    class Meta:
        model = NewsComment
        fields = [*create_comment_fields, 'news_item']
        extra_kwargs = {
            'news_item': {'write_only': True}
        }
        read_only_fields = ['rating']


class ListNewsCommentSerializer(ListCommentSerializerMixin):
    class Meta:
        model = NewsComment
        fields = [*list_comment_fields]

    source = serializers.SerializerMethodField()

    def get_rate(self, obj):
        if not self.context['request'].user.is_authenticated:
            return None
        found_rate = UserNewsCommentRelation.objects.filter(user=self.context['request'].user, comment=obj).first()
        if found_rate is None:
            return None
        return found_rate.rate

    def get_source(self, obj: NewsComment):
        return NewsSourceSerializer(obj.news_item).data


class CreateNewsCommentComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCommentComplaint
        fields = [*create_comment_complaint_fields]

    time_add = serializers.DateTimeField(format="%d.%m.%Y, %H:%M", read_only=True)


class RateNewsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNewsCommentRelation
        fields = ['rate', 'rating']
        read_only_fields = ['rating']

    rating = serializers.SerializerMethodField()

    def get_rating(self, obj: UserNewsCommentRelation):
        return obj.comment.rating

    def update(self, instance: UserNewsCommentRelation, validated_data):
        if instance.comment.is_deleted:
            raise NotAcceptable()

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
        UserAction.objects.create(action_type="rate_user", user=instance.user)
        return instance


class CreateBlogCommentSerializer(CreateCommentSerializerMixin):
    class Meta:
        model = BlogComment
        fields = [*create_comment_fields, 'blog_item']
        extra_kwargs = {
            'blog_item': {'write_only': True}
        }
        read_only_fields = ['rating']


class ListBlogCommentSerializer(ListCommentSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = [*list_comment_fields]

    source = serializers.SerializerMethodField()

    def get_rate(self, obj: BlogComment):
        if not self.context['request'].user.is_authenticated:
            return None
        found_rate = UserBlogCommentRelation.objects.filter(user=self.context['request'].user,  comment=obj).first()
        if found_rate is None:
            return None
        return found_rate.rate

    def get_source(self, obj: BlogComment):
        return BlogSourceSerializer(obj.blog_item).data


class CreateBlogCommentComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCommentComplaint
        fields = [*create_comment_complaint_fields]

    time_add = serializers.DateTimeField(format="%d.%m.%Y, %H:%M", read_only=True)


class RateBlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBlogCommentRelation
        fields = ['rate', 'rating']
        read_only_fields = ['rating']

    rating = serializers.SerializerMethodField()

    def get_rating(self, obj: UserBlogCommentRelation):
        return obj.comment.rating

    def update(self, instance: UserBlogCommentRelation, validated_data):
        if instance.comment.is_deleted:
            raise NotAcceptable()

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
        UserAction.objects.create(action_type="rate_user", user=instance.user)
        return instance
