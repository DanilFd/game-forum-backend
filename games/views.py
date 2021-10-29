from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from games.models import Game
from games.pagination import GamesPagination
from games.serializers import ListGameSerializer


class ListGameView(generics.ListAPIView):
    serializer_class = ListGameSerializer
    queryset = Game.objects.all()
    pagination_class = GamesPagination
