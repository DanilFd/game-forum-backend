# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from blogs.filters import BlogsFilterSet
from blogs.models import Blog
from blogs.pagination import BlogsPagination
from blogs.serializers import ListBlogSerializer, ContentImageSerializer
from rest_framework.views import APIView

from users.utils import get_web_url


class ListBlogView(generics.ListAPIView):
    serializer_class = ListBlogSerializer
    queryset = Blog.objects.all()
    pagination_class = BlogsPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BlogsFilterSet
    ordering_fields = ['rating']


class FileUploadAPI(generics.GenericAPIView):
    serializer_class = ContentImageSerializer

    def post(self, request):
        serializer = ContentImageSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        web_ulr = get_web_url(self.request)
        response = {
            "success": 1,
            "file": {
                "url": web_ulr + serializer.data['image']
            }
        }
        return Response(response)