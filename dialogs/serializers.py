from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable, NotFound

from dialogs.models import Dialog, DialogMessage, UnreadMessage
from users.models import CustomUser, UserAction
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

        message = DialogMessage.objects.create(sender=owner, dialog=dialog, content=validated_data["content"])
        UnreadMessage.objects.create(
            user=dialog.responder if owner == dialog.owner else dialog.owner, message=message)
        UserAction.objects.create(action_type="send_message", user=owner)
        return dialog


class SendMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DialogMessage
        fields = ['id', 'dialog', 'content', 'sender', 'sending_date', 'is_first']
        read_only_fields = ['sender', 'sending_date']

    sending_date = serializers.DateTimeField(format="%d.%m.%Y, %H:%M", read_only=True)
    sender = ModestUserProfileSerializer(read_only=True)
    is_first = serializers.SerializerMethodField()

    def get_is_first(self, obj: DialogMessage):
        return obj.id == obj.dialog.messages.earliest('sending_date').id

    def create(self, validated_data):
        print("kwargs:", validated_data)
        if not validated_data['dialog'].user_that_deleted is None:
            raise NotAcceptable(detail="Диалог удален")
        user = self.context['request'].user
        validated_data['sender'] = user
        message = super().create(validated_data)
        UnreadMessage.objects.create(
            user=validated_data['dialog'].responder if user == validated_data['dialog'].owner else validated_data[
                'dialog'].owner, message=message)
        return message


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
        fields = ['id', 'title', 'interlocutor', 'creation_date', 'last_message', 'messages_count']

    last_message = serializers.SerializerMethodField()
    interlocutor = serializers.SerializerMethodField()
    messages_count = serializers.SerializerMethodField()
    creation_date = serializers.DateTimeField(format="%d.%m.%Y, %H:%M")

    def get_last_message(self, obj: Dialog):
        return LastMessageSerializer(obj.messages.last(), context=self.context).data

    def get_messages_count(self, obj: Dialog):
        return obj.messages.count()

    def get_interlocutor(self, obj: Dialog):
        if self.context['request'].user == obj.responder:
            return ModestUserProfileSerializer(obj.owner, context=self.context).data
        return ModestUserProfileSerializer(obj.responder, context=self.context).data
