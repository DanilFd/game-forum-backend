from django.urls import path

from games.views import ListGameView, ListGenreView, ListPlatformView, FollowingOnGameView, GameDetailView

urlpatterns = [
    path('list/games/', ListGameView.as_view()),
    path('list/genres/', ListGenreView.as_view()),
    path('list/platforms/', ListPlatformView.as_view()),
    path('follow-and-unfollow/<int:pk>/', FollowingOnGameView.as_view()),
    path('detail/<str:slug>/', GameDetailView.as_view())
]
