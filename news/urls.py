from django.urls import path

from news.views import ListNewsItemView, ListCategoryNewsView, \
    DetailNewsItemView, FavoritesNewsView, SearchNewsView, ListNewsForGameDetailView, BestsForMonthNewsView, \
    DiscussedNewsForWeekView, LastsNewsView

urlpatterns = [
    path('list/news/', ListNewsItemView.as_view()),
    path('list/categories/', ListCategoryNewsView.as_view()),
    path('detail/news-item/<int:pk>/', DetailNewsItemView.as_view()),
    path('list/favorites-news/', FavoritesNewsView.as_view()),
    path('search/', SearchNewsView.as_view()),
    path('list/news-for-game/<int:pk>/', ListNewsForGameDetailView.as_view()),
    path('list/best-for-month/', BestsForMonthNewsView.as_view()),
    path('list/discussed-news/', DiscussedNewsForWeekView.as_view()),
    path('list/lasts-news/', LastsNewsView.as_view())
]
