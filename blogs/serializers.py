from rest_framework import serializers

from blogs.models import Blog
from games.utils.convert_month_to_str import convert_month_to_str
from users.serializers import ModestUserForBlogSerializer


class ListBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "img", "creation_date", "rating", "views_count", 'content', 'creator']

    creator = ModestUserForBlogSerializer()
    creation_date = serializers.DateField(format="%d.%m.%Y", read_only=True)
