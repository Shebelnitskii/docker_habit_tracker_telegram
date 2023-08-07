import requests
from django.core.management.base import BaseCommand
from config import settings
from main.models import Habit


class Command(BaseCommand):
    def handle(self, *args, **options):
        habit = Habit.objects.get(pk=1)

        message = (
            f"Напоминание о привычке для пользователя {habit.owner.username}:\n"
            f"Место: {habit.place}\n"
            f"Действие: {habit.action}\n"
            f"Время: {habit.time}"
        )
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
        params = {
            "chat_id": settings.CHAT_ID,
            "text": message
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("Сообщение успешно отправлено!")
        else:
            print("Произошла ошибка при отправке сообщения:")
            print(response.text)