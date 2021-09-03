# Create your views here.
from rest_framework import generics

from news.models import NewsItem
from news.serializers import CreateNewsItemSerializer, ListNewsItemSerializer


class CreateNewsItemView(generics.CreateAPIView):
    serializer_class = CreateNewsItemSerializer


class ListNewsItemView(generics.ListAPIView):
    serializer_class = ListNewsItemSerializer
    queryset = NewsItem.objects.all()
