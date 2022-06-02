# Create your views here.
from dateutil.relativedelta import relativedelta
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from blogs.filters import BlogsFilterSet
from blogs.models import Blog, BlogUserRelation
from blogs.pagination import BlogsPagination
from blogs.serializers import ListBlogSerializer, ContentImageSerializer, CreateBlogSerializer, ModestBlogsSerializer, \
    BlogDetailSerializer, RateBlogSerializer, BestBLogsSerializer
from users.models import UserAction
from users.permissions import get_permitted_rate_count, RateCountPermission, CantLikeSelfBLog
import datetime
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


class CreateBlogView(generics.CreateAPIView):
    serializer_class = CreateBlogSerializer
    permission_classes = [IsAuthenticated]


class SearchBlogsView(generics.ListAPIView):
    serializer_class = ModestBlogsSerializer
    queryset = Blog.objects.all()
    filter_backends = [filters.SearchFilter]
    pagination_class = BlogsPagination
    search_fields = ['title']


class BlogDetailView(generics.RetrieveAPIView):
    serializer_class = BlogDetailSerializer
    queryset = Blog.objects.all()

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj


class RateBlogView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, CantLikeSelfBLog, RateCountPermission]
    serializer_class = RateBlogSerializer

    def get_object(self):
        obj, _ = BlogUserRelation.objects.get_or_create(user=self.request.user,
                                                        blog=Blog.objects.get(id=self.kwargs['pk']))
        return obj

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        response.data['available_rate_count'] = get_permitted_rate_count(
            self.request.user.rating) - UserAction.objects.filter(user=self.request.user,
                                                                  moment__gt=datetime.date.today(),
                                                                  action_type="rate_user").count()
        return response


class BestsBlogsView(generics.ListAPIView):
    serializer_class = BestBLogsSerializer

    def get_queryset(self):
        return Blog.objects.filter(creation_date__gt=datetime.datetime.now() - relativedelta(weeks=1)).order_by(
            '-rating')[:6]
