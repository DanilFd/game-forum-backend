import requests
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import CustomUser
from users.serializers import CustomTokeObtainPairSerializer, UserProfileSerializer
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


class UserProfileView(generics.RetrieveAPIView):
    lookup_field = 'login'
    serializer_class = UserProfileSerializer
    queryset = CustomUser.objects.all()
