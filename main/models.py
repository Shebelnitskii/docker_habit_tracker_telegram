from django.db import models
from config import settings

NULLABLE = {'blank': True, 'null': True}


# Create your models here.

class Habit(models.Model):
    action = models.CharField(max_length=100, verbose_name='Действие')
    place = models.CharField(max_length=50, verbose_name='Место')
    time = models.TimeField(verbose_name='Время начала')
    time_to_complete = models.PositiveIntegerField(verbose_name='Время на выполнение(секундах)')
    periodicity = models.PositiveIntegerField(verbose_name='Периодичность привычки в днях')
    good_habit_sign = models.BooleanField(verbose_name='Полезность привычки')

    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE,
                                     verbose_name='Связанная привычка')
    reward = models.CharField(max_length=50, verbose_name='Награда', **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='Публичность')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Пользователь')
    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

class ChatState(models.Model):
    message_id = models.IntegerField(unique=True)
    message_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Chat ID: {self.chat_id}, Message Sent: {self.message_sent}"