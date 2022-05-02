from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from blogs.models import Blog
from blogs.pagination import BlogsPagination
from blogs.serializers import ListBlogSerializer


class ListBlogView(generics.ListAPIView):
    serializer_class = ListBlogSerializer
    queryset = Blog.objects.all()
    pagination_class = BlogsPagination
