from datetime import datetime

from django.utils import timezone
import requests
from django.core.management.base import BaseCommand
from config import settings
from main.models import ChatState, Habit
from users.models import User
from django.utils.crypto import get_random_string
import os
import django

# Установите переменную окружения DJANGO_SETTINGS_MODULE на путь к вашему модулю настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Настройте Django
django.setup()


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = datetime.now().time()

        for habit in Habit.objects.all():
            habit_time = habit.time
            if now.hour == habit_time.hour and now.minute == habit_time.minute:
                # Отправляем уведомление пользователю
                message = (
                    f"Напоминание о привычке для пользователя {habit.owner.username}:\n"
                    f"Место: {habit.place}\n"
                    f"Действие: {habit.action}\n"
                    f"Время: {habit.time}"
                )
                url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
                params = {
                    "chat_id": habit.owner.chat_id,
                    "text": message
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    print("Уведомление успешно отправлено")
                else:
                    print("Ошибка при отправке уведомления")