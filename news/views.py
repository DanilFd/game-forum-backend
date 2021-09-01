# Create your views here.
from rest_framework import generics

from news.models import NewsItem
from news.serializers import CreateNewsItemSerializer


class CreateNewsItemView(generics.CreateAPIView):
    serializer_class = CreateNewsItemSerializer


class ListNewsItemView(generics.ListAPIView):
    serializer_class = CreateNewsItemSerializer
    queryset = NewsItem.objects.all()
