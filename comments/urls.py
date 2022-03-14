from django.urls import path

from comments.views import CreateCommentView, ListNewsCommentView, CreateComplaintView, DeleteNewsCommentView, \
    RateCommentView


urlpatterns = [
    path('create/', CreateCommentView.as_view()),
    path('list/<int:pk>/', ListNewsCommentView.as_view()),
    path('complaint/create/', CreateComplaintView.as_view()),
    path('delete/<int:pk>/', DeleteNewsCommentView.as_view()),
    path('rate/<int:pk>/', RateCommentView.as_view())
]
