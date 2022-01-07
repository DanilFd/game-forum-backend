from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from dialogs.models import Dialog
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


class DialogsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DialogsListSerializer

    def get_queryset(self):
        return get_my_dialogs(self.request.user)


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
