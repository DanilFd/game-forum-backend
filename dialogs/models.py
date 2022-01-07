from django.db import models

# Create your models here.
from users.models import CustomUser


class Dialog(models.Model):
    class Meta:
        verbose_name = "Диалог"
        verbose_name_plural = "Диалоги"
        ordering = ['-id']

    title = models.CharField(verbose_name="Заголовок диалога", max_length=25)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_dialogs")
    responder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="responding_dialogs")
    creation_date = models.DateTimeField(auto_now_add=True)
    user_that_deleted = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.title


class DialogMessage(models.Model):
    class Meta:
        verbose_name = "Сообщения"
        verbose_name_plural = "Сообщения"
        ordering = ['sending_date']

    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    sending_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
