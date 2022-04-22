from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comments.models import NewsComment, UserCommentRelation
from comments.paginate_comments import paginate_comments
from comments.pagination import NewsCommentPagination
from comments.serializers import CreateCommentSerializer, ListNewsCommentSerializer, CreateComplaintSerializer, \
    RateCommentSerializer
from news.models import NewsItem
from users.models import UserAction
from users.permissions import CantLikeSelfComment, RateCountPermission, get_permitted_rate_count
import datetime


class CreateCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCommentSerializer


class ListNewsCommentView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginated_comments = paginate_comments(
            queryset,
            int(self.request.query_params.get('page', 1)),
            self.get_serializer_context()
        )
        return Response(paginated_comments)

    def get_queryset(self):
        return NewsComment.objects.filter(parent=None, news_item_id=self.kwargs['pk'])


class CreateComplaintView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateComplaintSerializer


class DeleteNewsCommentView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NewsComment.objects.filter(creator=self.request.user)

    def perform_destroy(self, instance: NewsComment):
        if not instance.children.count():
            return instance.delete()
        instance.is_deleted = True
        instance.save()


class RateCommentView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, CantLikeSelfComment, RateCountPermission]
    serializer_class = RateCommentSerializer

    def get_object(self):
        obj, _ = UserCommentRelation.objects.get_or_create(user=self.request.user,
                                                           comment=NewsComment.objects.get(id=self.kwargs['pk']))
        return obj

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        response.data['available_rate_count'] = get_permitted_rate_count(
            self.request.user.rating) - UserAction.objects.filter(user=self.request.user,
                                                                  moment__gt=datetime.date.today(),
                                                                  action_type="rate_user").count()
        return response
