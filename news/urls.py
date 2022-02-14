from django.urls import path

from news.views import ListNewsItemView, ListCategoryNewsView, \
    DetailNewsItemView, FavoritesNewsView

urlpatterns = [
    path('list/news/', ListNewsItemView.as_view()),
    path('list/categories/', ListCategoryNewsView.as_view()),
    path('detail/news-item/<int:pk>/', DetailNewsItemView.as_view()),
    path('list/favorites-news/', FavoritesNewsView.as_view())
]
