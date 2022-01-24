from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response

from dialogs.models import Dialog, UnreadMessage
from dialogs.serializers import CreateDialogSerializer, SendMessageSerializer, DialogDetailSerializer, \
    DialogsListSerializer
from users.models import CustomUser


def get_my_dialogs(me: CustomUser):
    return Dialog.objects.filter(Q(owner=me) | Q(responder=me))


class CreateDialogView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateDialogSerializer


class SendMessageView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SendMessageSerializer


class DialogDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DialogDetailSerializer

    def get_queryset(self):
        return get_my_dialogs(self.request.user)

    def get_object(self):
        dialog: Dialog = super().get_object()
        UnreadMessage.objects.filter(message__in=dialog.messages.all()).delete()
        return dialog


class DialogsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DialogsListSerializer

    def get_queryset(self):
        return get_my_dialogs(self.request.user).exclude(user_that_deleted=self.request.user)


class DeleteDialogView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_my_dialogs(self.request.user)

    def perform_destroy(self, instance: Dialog):
        if instance.user_that_deleted is None:
            instance.user_that_deleted = self.request.user
            instance.save()
        elif instance.user_that_deleted != self.request.user:
            instance.delete()


class GetNotifications(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        return Response({"unread_message_count": UnreadMessage.objects.filter(user=self.request.user).count()})
