from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokeObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['login'] = user.login
        token['role'] = user.role
        return token
