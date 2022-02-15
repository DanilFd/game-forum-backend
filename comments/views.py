from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from comments.models import NewsComment
from comments.pagination import NewsCommentPagination
from comments.serializers import CreateCommentSerializer, ListNewsCommentSerializer, CreateComplaintSerializer
from news.models import NewsItem


class CreateCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCommentSerializer


class ListNewsCommentView(generics.ListAPIView):
    serializer_class = ListNewsCommentSerializer
    pagination_class = NewsCommentPagination

    def get(self, request, *args, **kwargs):
        res = self.list(request, *args, **kwargs)
        res.data['comments_count'] = NewsItem.objects.get(id=self.kwargs['pk']).comments.count()
        return res

    def get_queryset(self):
        return NewsComment.objects.filter(parent=None, news_item_id=self.kwargs['pk'])


class CreateComplaintView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateComplaintSerializer


class DeleteNewsCommentView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NewsComment.objects.filter(creator=self.request.user)
