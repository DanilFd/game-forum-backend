from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comments.models import NewsComment, UserNewsCommentRelation, BlogComment, UserBlogCommentRelation
from comments.paginate_comments import paginate_comments
from comments.serializers import CreateNewsCommentSerializer, \
    CreateNewsCommentComplaintSerializer, \
    RateNewsCommentSerializer, CreateBlogCommentSerializer, CreateBlogCommentComplaintSerializer, \
    RateBlogCommentSerializer
from users.models import UserAction
from users.permissions import CantLikeSelfNewsComment, RateCountPermission, get_permitted_rate_count, \
    CantLikeSelfBlogComment
import datetime


class CreateNewsCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateNewsCommentSerializer


class CreateBlogCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateBlogCommentSerializer


class ListNewsCommentView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginated_comments = paginate_comments(
            queryset,
            int(self.request.query_params.get('page', 1)),
            self.get_serializer_context(),
            True
        )
        return Response(paginated_comments)

    def get_queryset(self):
        return NewsComment.objects.filter(parent=None, news_item_id=self.kwargs['pk'])


class ListBlogCommentView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginated_comments = paginate_comments(
            queryset,
            int(self.request.query_params.get('page', 1)),
            self.get_serializer_context(),
            False
        )
        return Response(paginated_comments)

    def get_queryset(self):
        return BlogComment.objects.filter(parent=None, blog_item_id=self.kwargs['pk'])


class CreateNewsCommentComplaintView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateNewsCommentComplaintSerializer


class CreateBlogCommentComplaintView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateBlogCommentComplaintSerializer


class DeleteNewsCommentView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NewsComment.objects.filter(creator=self.request.user)

    def perform_destroy(self, instance: NewsComment):
        if not instance.children.count():
            return instance.delete()
        instance.is_deleted = True
        instance.save()


class DeleteBlogCommentView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BlogComment.objects.filter(creator=self.request.user)

    def perform_destroy(self, instance: BlogComment):
        if not instance.children.count():
            return instance.delete()
        instance.is_deleted = True
        instance.save()


class RateNewsCommentView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, CantLikeSelfNewsComment, RateCountPermission]
    serializer_class = RateNewsCommentSerializer

    def get_object(self):
        obj, _ = UserNewsCommentRelation.objects.get_or_create(user=self.request.user,
                                                               comment=NewsComment.objects.get(
                                                                   id=self.kwargs['pk']))
        return obj

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        response.data['available_rate_count'] = get_permitted_rate_count(
            self.request.user.rating) - UserAction.objects.filter(user=self.request.user,
                                                                  moment__gt=datetime.date.today(),
                                                                  action_type="rate_user").count()
        return response


class RateBlogCommentView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, CantLikeSelfBlogComment, RateCountPermission]
    serializer_class = RateBlogCommentSerializer

    def get_object(self):
        obj, _ = UserBlogCommentRelation.objects.get_or_create(user=self.request.user,
                                                               comment=BlogComment.objects.get(
                                                                   id=self.kwargs['pk']))
        return obj

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        response.data['available_rate_count'] = get_permitted_rate_count(
            self.request.user.rating) - UserAction.objects.filter(user=self.request.user,
                                                                  moment__gt=datetime.date.today(),
                                                                  action_type="rate_user").count()
        return response
