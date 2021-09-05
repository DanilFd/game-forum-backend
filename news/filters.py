from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from news.models import NewsItem


class NewsFilterSet(FilterSet):
    class Meta:
        model = NewsItem
        fields = ["category"]
    category = CharFilter(field_name="category__slug")
