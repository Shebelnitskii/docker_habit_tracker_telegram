from django.db import models
from config import settings


# Create your models here.

class Habit(models.Model):
    CHOICES_PERIODICITY = (
        ('daily', 'Каждый день'),
        ('weekly', 'Каждую неделю'),
        ('monthly', 'Каждый месяц'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь')
    action = models.CharField(max_length=100, verbose_name='Действие')
    good_habit_sign = models.BooleanField(default=True, verbose_name='Полезность привычки')
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Связанная привычка')
    reward = models.CharField(max_length=50, verbose_name='Награда')
    is_public = models.BooleanField(default=False, verbose_name='Публичность')

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

class TimeAndPlace(models.Model):
    CHOICES_PERIODICITY = (
        ('daily', 'Каждый день'),
        ('weekly', 'Каждую неделю'),
        ('monthly', 'Каждый месяц'),
    )

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    time = models.TimeField(verbose_name='Время начала', default='12:00:00')
    periodicity = models.CharField(max_length=10, choices=CHOICES_PERIODICITY, verbose_name='Периодичность привычки',
                                   default='daily')
    place = models.CharField(max_length=50, verbose_name='Место')

    def __str__(self):
        return f'Время: {self.time}\nКак часто: {self.periodicity}'

    class Meta:
        verbose_name = 'Время отправки'
        verbose_name_plural = 'Время отправки'