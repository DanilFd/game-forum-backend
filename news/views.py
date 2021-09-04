# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from news.filters import NewsFilterSet
from news.models import NewsItem, NewsCategory
from news.serializers import CreateNewsItemSerializer, ListNewsItemSerializer, CreateCategoryNewsSerializer


class CreateNewsItemView(generics.CreateAPIView):
    serializer_class = CreateNewsItemSerializer


class ListNewsItemView(generics.ListAPIView):
    serializer_class = ListNewsItemSerializer
    queryset = NewsItem.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilterSet


class CreateCategoryNewsView(generics.CreateAPIView):
    serializer_class = CreateCategoryNewsSerializer


class ListCategoryNewsView(generics.ListAPIView):
    serializer_class = CreateCategoryNewsSerializer
    queryset = NewsCategory.objects.all()
