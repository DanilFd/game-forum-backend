from django.urls import path, include

from users.views import CustomTokeObtainPairView, UserActivationView, UserProfileView, UserProfileEditView, \
    CustomTokenRefreshView, UserListView, RateUserView, GetUserActionsView, IsRegisteredView, RegistrationByGoogleView

urlpatterns = [
    path('login/', CustomTokeObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>/', UserActivationView.as_view()),
    path('profile/edit/', UserProfileEditView.as_view()),
    path('profile/<slug:login>/', UserProfileView.as_view()),
    path('find/', UserListView.as_view()),
    path('rate/<str:username>/', RateUserView.as_view()),
    path('actions/', GetUserActionsView.as_view()),
    path('is-registered/<str:login>/', IsRegisteredView.as_view()),
    path('registration-by-google/', RegistrationByGoogleView.as_view())
]
