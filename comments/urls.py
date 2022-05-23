from django.urls import path

from comments.views import CreateNewsCommentView, ListNewsCommentView, CreateNewsCommentComplaintView, \
    DeleteNewsCommentView, \
    RateNewsCommentView, CreateBlogCommentView, ListBlogCommentView, CreateBlogCommentComplaintView, \
    DeleteBlogCommentView, RateBlogCommentView

urlpatterns = [
    path('news/create/', CreateNewsCommentView.as_view()),
    path('news/list/<int:pk>/', ListNewsCommentView.as_view()),
    path('news/complaint/create/', CreateNewsCommentComplaintView.as_view()),
    path('news/delete/<int:pk>/', DeleteNewsCommentView.as_view()),
    path('news/rate/<int:pk>/', RateNewsCommentView.as_view()),
    path('blog/create/', CreateBlogCommentView.as_view()),
    path('blog/list/<int:pk>/', ListBlogCommentView.as_view()),
    path('blog/complaint/create/', CreateBlogCommentComplaintView.as_view()),
    path('blog/delete/<int:pk>/', DeleteBlogCommentView.as_view()),
    path('blog/rate/<int:pk>/', RateBlogCommentView.as_view())
]
