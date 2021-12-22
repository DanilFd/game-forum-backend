from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

from users.models import CustomUser


class SetLastVisitMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            # Update last visit time after request finished processing.
            CustomUser.objects.filter(pk=request.user.pk).update(last_visit=now())
        return response
