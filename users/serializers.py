from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.utils import get_web_url


class CustomTokeObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        request = self.context['request']
        web_url = get_web_url(request)
        token = super().get_token(user)
        token['login'] = user.login
        token['role'] = user.role
        token['profile_img'] = web_url + user.profile_img.url
        return token