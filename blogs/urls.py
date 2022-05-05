from django.urls import path

from blogs.views import ListBlogView, FileUploadAPI, CreateBlogView

urlpatterns = [
    path('list/all/', ListBlogView.as_view()),
    path('upload-img/', FileUploadAPI.as_view()),
    path('create/', CreateBlogView.as_view())
]
