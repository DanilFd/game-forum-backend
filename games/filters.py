import django_filters
from django_filters.rest_framework import FilterSet

from games.models import Game, Genre, Platform


class GamesFilterSet(FilterSet):
    class Meta:
        model = Game
        fields = []

    genre = django_filters.ModelMultipleChoiceFilter(
        field_name="genres__slug",
        to_field_name='slug',
        conjoined=True,
        queryset=Genre.objects.all()
    )
    platform = django_filters.ModelMultipleChoiceFilter(
        field_name="platforms__slug",
        to_field_name="slug",
        conjoined=True,
        queryset=Platform.objects.all()
    )
    year_start = django_filters.NumberFilter(
        field_name="release_date__year",
        lookup_expr='gte'
    )
    year_end = django_filters.NumberFilter(
        field_name="release_date__year",
        lookup_expr='lte'
    )
