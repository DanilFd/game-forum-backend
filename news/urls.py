from django.urls import path

from news.views import CreateNewsItemView, ListNewsItemView

urlpatterns = [
    path('create/', CreateNewsItemView.as_view()),
    path('', ListNewsItemView.as_view())
]
