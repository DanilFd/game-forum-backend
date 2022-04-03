import datetime

import requests
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.models import CustomUser, UserUserRelation, UserAction
from users.permissions import get_permitted_messages_count, RateCountPermission, get_permitted_rate_count, CantLikeSelf
from users.serializers import CustomTokeObtainPairSerializer, UserProfileSerializer, UserProfileEditSerializer, \
    CustomTokenRefreshSerializer, ModestUserSerializer, RateUserSerializer, RegistrationByGoogleSerializer
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