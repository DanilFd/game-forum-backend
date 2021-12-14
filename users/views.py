import requests
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import CustomUser
from users.serializers import CustomTokeObtainPairSerializer


class UserActivationView(APIView):
    def post(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/api/users/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        uid = force_text(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(pk=uid)

        def get_tokens_for_user(user):
            refresh = RefreshToken.for_user(user)
            refresh['login'] = user.login
            refresh['role'] = user.role
            refresh['test'] = 'nigres'
            print('refresh:', refresh.access_token)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        requests.post(post_url, data=post_data)
        return Response(get_tokens_for_user(user))


class CustomTokeObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokeObtainPairSerializer
