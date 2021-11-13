from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from games.models import Game
from news.models import NewsItem


class GamesFilterSet(FilterSet):
    class Meta:
        model = Game
        fields = ["genres"]
    genre = CharFilter(field_name="genres__title")

