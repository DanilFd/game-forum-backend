# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from news.filters import NewsFilterSet
from news.models import NewsItem, NewsCategory
from news.serializers import ListNewsItemSerializer, \
    DetailNewsItemSerializer, ListNewsCategoriesSerializer


class ListNewsItemView(generics.ListAPIView):
    serializer_class = ListNewsItemSerializer
    queryset = NewsItem.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilterSet


class ListCategoryNewsView(generics.ListAPIView):
    serializer_class = ListNewsCategoriesSerializer
    queryset = NewsCategory.objects.all()


class DetailNewsItemView(generics.RetrieveAPIView):
    serializer_class = DetailNewsItemSerializer
    queryset = NewsItem.objects.all()
