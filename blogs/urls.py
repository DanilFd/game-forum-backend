from django.urls import path

from blogs.views import ListBlogView, FileUploadAPI

urlpatterns = [
    path('list/all/', ListBlogView.as_view()),
    path('upload-img/', FileUploadAPI.as_view())
]
