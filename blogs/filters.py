import django_filters
from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from blogs.models import Blog


class BlogsFilterSet(FilterSet):
    class Meta:
        model = Blog
        fields = ["creation_date"]

    creation_date = django_filters.DateFromToRangeFilter()
    creator = CharFilter(field_name="creator__login")
