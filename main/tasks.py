from celery import shared_task
import requests
from django.conf import settings

from main.models import ChatState
from users.models import User
from django.utils.crypto import get_random_string


@shared_task
def start_message():
    url_updates = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/getupdates"
    response = requests.get(url_updates)
    data = response.json()
    for item in data['result']:
        message = item['message']
        if 'text' in message and message['text'] == '/start':
            message_id = message['message_id']
            if not ChatState.objects.filter(message_id=message_id, message_sent=True).exists():
                chat_id = message['chat']['id']
                first_name = message['from']['first_name']
                username = message['from']['username']

                print(f"Найдено сообщение с текстом '/start'")
                print(f"Username: {username}, Chat ID: {chat_id}")

                text = (
                    f"Добро пожаловать в мой скромный бот: {first_name}\n"
                    f"Для регистрации введите команду\n/registration\n"
                )
                url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
                params = {
                    "chat_id": chat_id,
                    "text": text
                }
                response = requests.get(url, params=params)
                if response.status_code != 200:
                    print("Ошибка при отправке сообщения в Telegram")
                else:
                    ChatState.objects.create(message_id=message_id, message_sent=True)


@shared_task
def registration_message():
    url_updates = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/getupdates"
    response = requests.get(url_updates)
    data = response.json()
    for item in data['result']:
        message = item['message']
        if 'text' in message and message['text'] == '/registration':
            message_id = message['message_id']
            if not ChatState.objects.filter(message_id=message_id, message_sent=True).exists():
                chat_id = message['chat']['id']
                username = message['from']['username']
                # Создаем нового пользователя
                password = get_random_string(length=10)  # Генерируем случайный пароль
                User.objects.create_user(username=username, password=password, chat_id=chat_id)

                # Отправляем сообщение пользователю
                message = (
                    f"Регистрация успешно выполнена, ваш пароль для работы с API: {password}\nЛогин для работы с API: {username}"
                    f"Для работы с API можете использовать Postman, Insomnia, Swagger и др."
                )
                url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
                params = {
                    "chat_id": chat_id,
                    "text": message
                }
                response = requests.get(url, params=params)
                if response.status_code != 200:
                    print("Ошибка при отправке сообщения в Telegram")
                else:
                    ChatState.objects.create(message_id=message_id, message_sent=True)
