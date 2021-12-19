from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import CustomTokeObtainPairView, UserActivationView, UserProfileView

urlpatterns = [
    path('login/', CustomTokeObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>/', UserActivationView.as_view()),
    path('profile/<slug:login>/', UserProfileView.as_view())
]
