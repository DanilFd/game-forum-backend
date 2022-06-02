# Create your views here.
import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from comments.models import NewsComment
from news.filters import NewsFilterSet
from news.models import NewsItem, NewsCategory
from news.pagination import NewsPagination
from news.serializers import ListNewsItemSerializer, \
    DetailNewsItemSerializer, ListNewsCategoriesSerializer, FavoritesNewsSerializer, ModestNewsListSerializer, \
    BestsForMonthNewsSerializer, DiscussedNewsForWeekSerializer, LastsNewsSerializer


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
    serializer_class = ModestNewsListSerializer
    queryset = NewsItem.objects.all()
    filter_backends = [filters.SearchFilter]
    pagination_class = NewsPagination
    search_fields = ['title']


class ListNewsForGameDetailView(generics.ListAPIView):
    serializer_class = ListNewsItemSerializer

    def get_queryset(self):
        return NewsItem.objects.filter(games__in=[self.kwargs['pk']])


class BestsForMonthNewsView(generics.ListAPIView):
    serializer_class = BestsForMonthNewsSerializer

    def get_queryset(self):
        return NewsItem.objects.filter(creation_date__gt=datetime.datetime.now() - relativedelta(months=1)).order_by(
            '-views_count')[:5]


class DiscussedNewsForWeekView(generics.ListAPIView):
    serializer_class = DiscussedNewsForWeekSerializer

    def get_queryset(self):
        return NewsItem.objects.filter(
            creation_date__gt=datetime.datetime.now() - relativedelta(weeks=1)).annotate(
            comments_count=Count("news_comments")).order_by('-comments_count')[:6]


class LastsNewsView(generics.ListAPIView):
    serializer_class = LastsNewsSerializer

    def get_queryset(self):
        return NewsItem.objects.filter().order_by('-creation_date')[:6]
