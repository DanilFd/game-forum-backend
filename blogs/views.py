# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from blogs.filters import BlogsFilterSet
from blogs.models import Blog
from blogs.pagination import BlogsPagination
from blogs.serializers import ListBlogSerializer


class ListBlogView(generics.ListAPIView):
    serializer_class = ListBlogSerializer
    queryset = Blog.objects.all()
    pagination_class = BlogsPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BlogsFilterSet
    ordering_fields = ['rating']
