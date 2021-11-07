from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from games.models import Game
from games.pagination import GamesPagination
from games.serializers import ListGameSerializer


class ListGameView(generics.ListAPIView):
    serializer_class = ListGameSerializer
    queryset = Game.objects.all()
    pagination_class = GamesPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        response.data['min_data'] = Game.objects.earliest('release_date').release_date.year
        response.data['max_data'] = Game.objects.latest('release_date').release_date.year
        return response
