from django.urls import path

from games.views import ListGameView

urlpatterns = [
    path('list/games/', ListGameView.as_view())
]
