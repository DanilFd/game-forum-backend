from django.urls import path

from blogs.views import ListBlogView, FileUploadAPI, CreateBlogView, SearchBlogsView, BlogDetailView, RateBlogView

urlpatterns = [
    path('list/all/', ListBlogView.as_view()),
    path('upload-img/', FileUploadAPI.as_view()),
    path('create/', CreateBlogView.as_view()),
    path('search/', SearchBlogsView.as_view()),
    path('detail/<int:pk>/', BlogDetailView.as_view()),
    path('rate/<int:pk>/', RateBlogView.as_view())
]
