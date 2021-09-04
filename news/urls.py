from django.urls import path

from news.views import CreateNewsItemView, ListNewsItemView, CreateCategoryNewsView, ListCategoryNewsView

urlpatterns = [
    path('create/news-item/', CreateNewsItemView.as_view()),
    path('list/news/', ListNewsItemView.as_view()),
    path('create/category/', CreateCategoryNewsView.as_view()),
    path('list/categories/', ListCategoryNewsView.as_view())
]
