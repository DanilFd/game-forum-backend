from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from games.filters import GamesFilterSet
from games.models import Game, Genre, Platform
from games.pagination import GamesPagination
from games.serializers import ListGameSerializer, ListGenreSerializer, ListPlatformSerializer


class ListGameView(generics.ListAPIView):
    serializer_class = ListGameSerializer
    queryset = Game.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = GamesFilterSet
    pagination_class = GamesPagination
    ordering_fields = ('release_date', 'score')

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['min_date'] = Game.objects.earliest('release_date').release_date.year
        response.data['max_date'] = Game.objects.latest('release_date').release_date.year
        return response


class ListGenreView(generics.ListAPIView):
    serializer_class = ListGenreSerializer
    queryset = Genre.objects.all()


class ListPlatformView(generics.ListAPIView):
    serializer_class = ListPlatformSerializer
    queryset = Platform.objects.all()
