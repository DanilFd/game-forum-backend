from django.urls import path

from dialogs.views import CreateDialogView, SendMessageView, DialogDetailView, DialogsListView, DeleteDialogView

urlpatterns = [
    path('create/', CreateDialogView.as_view()),
    path('send/', SendMessageView.as_view()),
    path('<int:pk>/', DialogDetailView.as_view()),
    path('get/', DialogsListView.as_view()),
    path('delete/<int:pk>/', DeleteDialogView.as_view()),
]
