# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from games.serializers import GameSerializer
from news.filters import NewsFilterSet
from news.models import NewsItem, NewsCategory
from news.pagination import NewsPagination
from news.serializers import ListNewsItemSerializer, \
    DetailNewsItemSerializer, ListNewsCategoriesSerializer, FavoritesNewsSerializer


class ListNewsItemView(generics.ListAPIView):
    serializer_class = ListNewsItemSerializer
    queryset = NewsItem.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilterSet
    pagination_class = NewsPagination


class ListCategoryNewsView(generics.ListAPIView):
    serializer_class = ListNewsCategoriesSerializer
    queryset = NewsCategory.objects.all()


class DetailNewsItemView(generics.RetrieveAPIView):
    serializer_class = DetailNewsItemSerializer
    queryset = NewsItem.objects.all()

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj


class FavoritesNewsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritesNewsSerializer
    pagination_class = NewsPagination

    def get_queryset(self):
        return NewsItem.objects.filter(games__user_relations__is_following=True,
                                       games__user_relations__user=self.request.user).distinct()


class SearchNewsView(generics.ListAPIView):
    serializer_class = ListNewsItemSerializer
    queryset = NewsItem.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
