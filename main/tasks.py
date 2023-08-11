from datetime import datetime

from celery import shared_task
import requests
from django.conf import settings
from django.db.models import Q
from main.models import ChatState, Habit
from users.models import User
from django.utils.crypto import get_random_string


@shared_task
def start_message():
    url_updates = (
        f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/getupdates"
    )
    response = requests.get(url_updates)
    data = response.json()
    for item in data["result"]:
        try:
            message = item["message"]
            if "text" in message and message["text"] == "/start":
                message_id = message["message_id"]
                if not ChatState.objects.filter(
                    message_id=message_id, message_sent=True
                ).exists():
                    chat_id = message["chat"]["id"]
                    first_name = message["from"]["first_name"]
                    username = message["from"]["username"]
                    try:
                        user = User.objects.filter(
                            Q(chat_id=chat_id) | Q(username=username)
                        )
                        text = "Вы уже запустили бота"
                    except:
                        text = (
                            f"Добро пожаловать в мой скромный бот: {first_name}\n"
                            f"Для регистрации введите команду\n/registration\n"
                        )
                    url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
                    params = {"chat_id": chat_id, "text": text}
                    response = requests.get(url, params=params)
                    if response.status_code != 200:
                        print("Ошибка при отправке сообщения в Telegram")
                    else:
                        ChatState.objects.create(
                            message_id=message_id, message_sent=True
                        )
        except:
            print(f"Нет ключа ['message'] в update_id {item['update_id']}")


@shared_task
def registration_message():
    url_updates = (
        f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/getupdates"
    )
    response = requests.get(url_updates)
    data = response.json()
    for item in data["result"]:
        try:
            message = item["message"]
            if "text" in message and message["text"] == "/registration":
                message_id = message["message_id"]
                if not ChatState.objects.filter(
                    message_id=message_id, message_sent=True
                ).exists():
                    chat_id = message["chat"]["id"]
                    username = message["from"]["username"]
                    # try:
                    #     user = User.objects.filter(Q(chat_id=chat_id) | Q(username=username))
                    #     text = "Вы уже зарегистрированы"
                    # except :
                    # Создаем нового пользователя
                    # Генерируем случайный пароль
                    password = get_random_string(length=10)
                    User.objects.create_user(
                        username=username, password=password, chat_id=chat_id
                    )

                    # Отправляем сообщение пользователю
                    text = (
                        f"Регистрация успешно выполнена, ваш пароль для работы с API: {password}\nЛогин для работы с API: {username}\n"
                        f"Для работы с API можете использовать Postman, Insomnia, Swagger и др."
                    )
                    # Отправляем сообщение
                    url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
                    params = {"chat_id": chat_id, "text": text}
                    response = requests.get(url, params=params)
                    if response.status_code != 200:
                        print("Ошибка при отправке сообщения в Telegram")
                    else:
                        ChatState.objects.create(
                            message_id=message_id, message_sent=True
                        )
        except:
            print(f"Нет ключа ['message'] в update_id {item['update_id']}")


@shared_task
def send_habit_message():
    now = datetime.now().time()

    for habit in Habit.objects.all():
        habit_time = habit.time
        if now.hour == habit_time.hour and now.minute == habit_time.minute:
            # Отправляем уведомление пользователю
            text = (
                f"Напоминание о привычке для пользователя {habit.owner.username}:\n"
                f"Место: {habit.place}\n"
                f"Действие: {habit.action}\n"
                f"Время: {habit.time}"
            )
            url = (
                f"https://api.telegram.org/bot{settings.TELEGRAM_API_TOKEN}/sendMessage"
            )
            params = {"chat_id": habit.owner.chat_id, "text": text}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                print("Уведомление успешно отправлено")
            else:
                print("Ошибка при отправке уведомления")
