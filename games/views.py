from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from games.filters import GamesFilterSet
from games.game_serializer import ListGameSerializer
from games.models import Game, Genre, Platform, UserGameRelation
from games.pagination import GamesPagination
from games.serializers import ListGenreSerializer, ListPlatformSerializer, UserGameRelationSerializer, \
    GameDetailSerializer, ModestGameSerializer


class ListGameView(generics.ListAPIView):
    serializer_class = ListGameSerializer
    queryset = Game.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = GamesFilterSet
    pagination_class = GamesPagination
    ordering_fields = ('release_date', 'rating')

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


class FollowingOnGameView(generics.UpdateAPIView):
    serializer_class = UserGameRelationSerializer
    queryset = UserGameRelation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj, _ = UserGameRelation.objects.get_or_create(user=self.request.user, game_id=self.kwargs['pk'])
        return obj


class GameDetailView(generics.RetrieveAPIView):
    serializer_class = GameDetailSerializer
    queryset = Game.objects.all()
    lookup_field = 'slug'


class SearchGamesView(generics.ListAPIView):
    serializer_class = ModestGameSerializer
    queryset = Game.objects.all()
    filter_backends = [filters.SearchFilter]
    pagination_class = GamesPagination
    search_fields = ['title']
