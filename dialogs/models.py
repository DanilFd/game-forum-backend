from django.db import models

# Create your models here.
from users.models import CustomUser


class Dialog(models.Model):
    class Meta:
        verbose_name = "Диалог"
        verbose_name_plural = "Диалоги"
        ordering = ['-id']

    title = models.CharField(verbose_name="Заголовок диалога", max_length=50)
    owner = models.ForeignKey(CustomUser, verbose_name='Создатель диалога', on_delete=models.CASCADE,
                              related_name="created_dialogs")
    responder = models.ForeignKey(CustomUser, verbose_name='Получатель', on_delete=models.CASCADE,
                                  related_name="responding_dialogs")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    user_that_deleted = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.title


class DialogMessage(models.Model):
    class Meta:
        verbose_name = "Сообщения"
        verbose_name_plural = "Сообщения"
        ordering = ['sending_date']

    sender = models.ForeignKey(CustomUser, verbose_name='Отправитель', on_delete=models.CASCADE)
    dialog = models.ForeignKey(Dialog, verbose_name='Диалог', on_delete=models.CASCADE, related_name="messages")
    content = models.TextField(verbose_name='Контент', max_length=150)
    sending_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    def __str__(self):
        return self.content


class UnreadMessage(models.Model):
    class Meta:
        pass

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.ForeignKey(DialogMessage, on_delete=models.CASCADE, related_name="unread_messages")
