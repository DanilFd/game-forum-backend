from rest_framework.permissions import BasePermission
import datetime

from users.models import UserAction, UserUserRelation


def get_permitted_messages_count(rating):
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


def get_permitted_rate_count(rating):
    if rating > 100:
        return 30
    if rating > 50:
        return 20
    if rating > 0:
        return 10
    if rating <= 0:
        return 5


class RateCountPermission(BasePermission):
    message = "Вы превыслили ваш лимит голосований за сутки."

    def has_permission(self, request, view):
        rate_count = UserAction.objects.filter(user=request.user, moment__gt=datetime.date.today(),
                                               action_type='rate_user').count()

        return rate_count != get_permitted_rate_count(request.user.rating)


class CantLikeSelf(BasePermission):
    message = "Вы не можете оценить себя."

    def has_permission(self, request, view):

        return request.user.login != view.kwargs['username']
