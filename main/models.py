from django.db import models
from config import settings

NULLABLE = {'blank': True, 'null': True}


# Create your models here.

class Habit(models.Model):
    action = models.CharField(max_length=100, verbose_name='Действие')
    good_habit_sign = models.BooleanField(verbose_name='Полезность привычки')
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE,
                                     verbose_name='Связанная привычка')
    reward = models.CharField(max_length=50, verbose_name='Награда', **NULLABLE)
    is_public = models.BooleanField(verbose_name='Публичность')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Пользователь')
    time = models.TimeField(verbose_name='Время начала')
    time_to_complete = models.PositiveIntegerField(verbose_name='Время на выполнение(секундах)')
    periodicity = models.PositiveIntegerField(verbose_name='Периодичность привычки в днях')
    place = models.CharField(max_length=50, verbose_name='Место')

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
