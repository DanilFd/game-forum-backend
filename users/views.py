import datetime

import requests

# Create your views here.
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from blogs.models import Blog
from blogs.serializers import ListBlogSerializer
from comments.models import NewsComment, BlogComment
from comments.serializers import ListNewsCommentSerializer, ListBlogCommentSerializer
from games.game_serializer import ListGameSerializer
from games.models import Game
from users.models import CustomUser, UserUserRelation, UserAction
from users.pagination import UsersPagination
from users.permissions import get_permitted_messages_count, RateCountPermission, get_permitted_rate_count, CantLikeSelf
from users.serializers import CustomTokeObtainPairSerializer, UserProfileEditSerializer, \
    CustomTokenRefreshSerializer, ModestUserSerializer, RateUserSerializer, RegistrationByGoogleSerializer, \
    ModestUserForSearchSerializer
from users.user_profile_serializer import UserProfileSerializer
from users.utils import get_web_url


class UserActivationView(APIView):
    def post(self, request, uid, token):
        web_url = get_web_url(self.request)
        post_url = web_url + "/api/users/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        uid = force_text(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(pk=uid)

        def get_tokens_for_user(user):
            refresh = RefreshToken.for_user(user)
            refresh['login'] = user.login
            refresh['role'] = user.role
            refresh['profile_img'] = web_url + user.profile_img.url
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        requests.post(post_url, data=post_data)
        return Response(get_tokens_for_user(user))


class CustomTokeObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokeObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class UserProfileView(generics.RetrieveAPIView):
    lookup_field = 'login'
    serializer_class = UserProfileSerializer
    queryset = CustomUser.objects.all()


class UserProfileEditView(generics.UpdateAPIView):
    serializer_class = UserProfileEditSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    serializer_class = ModestUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['login']


class RateUserView(generics.UpdateAPIView):
    serializer_class = RateUserSerializer
    permission_classes = {IsAuthenticated, RateCountPermission, CantLikeSelf}

    def get_object(self):
        obj, _ = UserUserRelation.objects.get_or_create(user2=self.request.user,
                                                        user1=CustomUser.objects.get(login=self.kwargs['username']))
        return obj

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        response.data['available_rate_count'] = get_permitted_rate_count(
            self.request.user.rating) - UserAction.objects.filter(user=self.request.user,
                                                                  moment__gt=datetime.date.today(),
                                                                  action_type="rate_user").count()
        return response


class GetUserActionsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = dict(
            available_messages=get_permitted_messages_count(request.user.rating)
        )
        return Response(data)


class IsRegisteredView(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        return Response(bool(CustomUser.objects.filter(login=self.kwargs['login']).first()))


class RegistrationByGoogleView(generics.CreateAPIView):
    serializer_class = RegistrationByGoogleSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        web_url = get_web_url(self.request)
        user = CustomUser.objects.get(login=self.request.data['login'])

        def get_tokens_for_user():
            refresh = RefreshToken.for_user(user)
            refresh['login'] = user.login
            refresh['role'] = user.role
            refresh['profile_img'] = web_url + user.profile_img.url
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        return Response(get_tokens_for_user())


class SearchUserView(generics.ListAPIView):
    serializer_class = ModestUserForSearchSerializer
    queryset = CustomUser.objects.all()
    filter_backends = [filters.SearchFilter]
    pagination_class = UsersPagination
    search_fields = ['login']


class UserBlogsListView(generics.ListAPIView):
    pagination_class = UsersPagination
    serializer_class = ListBlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(creator=self.kwargs['pk'])


class UserCommentsListView(generics.ListAPIView):
    queryset = ()

    def get(self, request, *args, **kwargs):
        comments = [
            *ListNewsCommentSerializer(NewsComment.objects.filter(creator=self.kwargs['pk']), many=True,
                                       context=self.get_serializer_context()).data,
            *ListBlogCommentSerializer(BlogComment.objects.filter(creator=self.kwargs['pk']), many=True,
                                       context=self.get_serializer_context()).data]
        comments = sorted(comments,
                          key=lambda c: datetime.datetime.strptime(c['creation_date'], "%d.%m.%Y, %H:%M"),
                          reverse=True)
        paginator = Paginator(comments, 10)
        page = self.request.query_params.get('page', 1)
        try:
            paginated_comments = paginator.page(page)
        except PageNotAnInteger:
            paginated_comments = paginator.page(1)
        except EmptyPage:
            return Response(dict(detail="Неправильная страница"))
        return Response(dict(result=list(paginated_comments), count=paginator.count))


class ListUserFavoriteGameView(generics.ListAPIView):
    serializer_class = ListGameSerializer
    pagination_class = UsersPagination

    def get_queryset(self):
        return Game.objects.filter(user_relations__user=self.kwargs['pk'], user_relations__is_following=True)


class ListUserRatedGameView(generics.ListAPIView):
    serializer_class = ListGameSerializer
    pagination_class = UsersPagination

    def get_queryset(self):
        return Game.objects.filter(user_relations__user=self.kwargs['pk']).exclude(user_relations__rate__isnull=True)
