import requests
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import CustomUser
from users.serializers import CustomTokeObtainPairSerializer


# class RegisterUserView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = RegisterUserSerializer
#     permission_classes = (AllowAny,)


class UserActivationView(APIView):
    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/api/users/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        requests.post(post_url, data=post_data)
        return redirect(protocol + 'localhost:3000')


class CustomTokeObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokeObtainPairSerializer
