from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable, NotFound

from dialogs.models import Dialog, DialogMessage
from users.models import CustomUser
from users.serializers import ModestUserProfileSerializer


class CreateDialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialog
        fields = ['title', 'responder', 'content']

    content = serializers.CharField(write_only=True)
    responder = serializers.CharField(max_length=20, min_length=6)

    def create(self, validated_data):
        owner = self.context['request'].user
        responder = CustomUser.objects.filter(login=validated_data["responder"]).first()
        if responder is None:
            raise NotFound(detail="Пользователь не найден.")
        if responder.login == owner.login:
            raise NotAcceptable(detail="Вы не можете написать самому себе.")
        dialog = Dialog.objects.create(title=validated_data["title"], owner=owner,
                                       responder=responder)
        DialogMessage.objects.create(sender=owner, dialog=dialog, content=validated_data["content"])
        return dialog


class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DialogMessage
        fields = ['dialog', 'content', 'sender', 'sending_date']
        read_only_fields = ['sender', 'sending_date']

    sending_date = serializers.DateTimeField(format="%d.%m.%Y, %H:%M")
    sender = ModestUserProfileSerializer()

    def save(self, **kwargs):
        if not kwargs['dialog'].user_that_deleted is None:
            raise NotAcceptable(detail="Диалог удален")
        super().save(**kwargs, sender=self.context['request'].user)


class DialogDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialog
        fields = ['title', 'messages', 'user_that_deleted']

    messages = SendMessageSerializer(many=True)


class LastMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DialogMessage
        fields = ['content', 'is_me']

    is_me = serializers.SerializerMethodField()

    def get_is_me(self, obj: DialogMessage):
        return obj.sender.login == self.context['request'].user.login


class DialogsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialog
        fields = ['id', 'title', 'responder', 'creation_date', 'last_message', 'messages_count']

    last_message = serializers.SerializerMethodField()
    responder = ModestUserProfileSerializer()
    messages_count = serializers.SerializerMethodField()

    def get_last_message(self, obj: Dialog):
        return LastMessageSerializer(obj.messages.last(), context=self.context).data

    def get_messages_count(self, obj: Dialog):
        return obj.messages.count()
