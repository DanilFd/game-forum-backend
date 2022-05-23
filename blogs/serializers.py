from decimal import Decimal

from rest_framework import serializers

from blogs.models import Blog, ContentImage, BlogUserRelation
from users.models import UserAction
from users.serializers import ModestUserForBlogSerializer, ModestUserProfileSerializer


class ListBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "img", "creation_date", "rating", "views_count", 'content', 'creator']

    creator = ModestUserForBlogSerializer()


class ContentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentImage
        fields = ['image']


class CreateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["title", "img", 'content', 'creator']

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class ModestBlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'img', 'creation_date']

    creation_date = serializers.DateTimeField(format="%d.%m.%Y", read_only=True)


class BlogDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "creation_date", "rating", "views_count", 'content', 'creator', 'rate']

    creator = ModestUserProfileSerializer()
    rate = serializers.SerializerMethodField()

    def get_rate(self, obj: Blog):
        if not self.context['request'].user.is_authenticated:
            return None
        found_rate = BlogUserRelation.objects.filter(user=self.context['request'].user, blog=obj).first()
        if found_rate is None:
            return None
        return found_rate.rate


class RateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUserRelation
        fields = ['rate', 'rating']
        read_only_fields = ['rating']

    rating = serializers.SerializerMethodField()

    def get_rating(self, obj: BlogUserRelation):
        return obj.blog.rating

    def update(self, instance: BlogUserRelation, validated_data):

        initial_rate = instance.rate
        instance.rate = validated_data['rate']
        instance.save()
        if initial_rate == 'Like':
            if instance.rate == 'Dislike':
                instance.user.rating -= Decimal(0.5)
                instance.blog.rating -= 2

            elif instance.rate is None:
                instance.user.rating -= Decimal(0.50)
                instance.blog.rating -= 1

        elif initial_rate == 'Dislike':
            if instance.rate == 'Like':
                instance.user.rating += Decimal(0.50)
                instance.blog.rating += 2

            elif instance.rate is None:
                instance.user.rating += Decimal(0.50)
                instance.blog.rating += 1

        elif initial_rate is None:
            if instance.rate == 'Like':
                instance.user.rating += Decimal(0.50)
                instance.blog.rating += 1

            elif instance.rate == 'Dislike':
                instance.user.rating -= Decimal(0.50)
                instance.blog.rating -= 1

        instance.blog.save()
        instance.user.save()
        UserAction.objects.create(action_type="rate_user", user=instance.user)
        return instance


class BlogSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title']
