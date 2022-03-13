from rest_framework.permissions import BasePermission
import datetime

from users.models import UserAction


def get_permitted_messages_count(rating: float):
    if rating > 100:
        return 12
    if rating > 50:
        return 6
    if rating > 0:
        return 4
    if rating < 0:
        return 2


class MessageCountPermission(BasePermission):
    message = f"Ваш лимит на создание диалогов исчерпан."

    def has_permission(self, request, view):
        messages_count = UserAction.objects.filter(user=request.user, moment__gt=datetime.date.today(),
                                                   action_type='send_message').count()

        return messages_count != get_permitted_messages_count(request.user.rating)
