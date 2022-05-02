from django.urls import path

from blogs.views import ListBlogView

urlpatterns = [
    path('list/all/', ListBlogView.as_view()),
]
