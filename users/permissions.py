from rest_framework.permissions import BasePermission
import datetime

from users.models import UserAction


def get_permitted_messages_count(rating: float):
    if rating < 40:
        return 2
    if rating > 40:
        return 5
    if rating > 75:
        return 10


class MessageCountPermission(BasePermission):
    message = f"Ваш лимит на создание диалогов исчерпан."

    def has_permission(self, request, view):
        messages_count = UserAction.objects.filter(user=request.user, moment__gt=datetime.date.today(),
                                                   action_type='send_message').count()

        return messages_count != get_permitted_messages_count(request.user.rating)
