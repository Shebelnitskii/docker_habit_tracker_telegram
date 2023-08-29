Проект "Shebelnitskiy Habit Tracker" представляет собой веб-приложение для отслеживания привычек через Telegram бота.

## Требования

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Установка
Клонируйте репозиторий на свой компьютер:
- git clone https://github.com/Shebelnitskii/django_habit_tracker_telegram

Перейдите в директорию проекта:
- cd django_habit_tracker_telegram

Создайте и активируйте виртуальное окружение:
- python -m venv venv
- source venv/bin/activate

Установите зависимости из файла requirements.txt:
- pip install -r requirements.txt

Настройка:
- Создайте файл .env в корневой директории проекта и скопируйте в него содержимое из .env.sample. Заполните необходимые параметры, такие как TELEGRAM_API_TOKEN

## Запуск проекта
1. #### Сделайте миграцию внутри контейнера через команду:
   - docker-compose exec <имя контейнера если оно было изменено вами> python manage.py migrate      
2. #### Соберите Docker образы и запустите контейнеры:
    - docker-compose build
    - docker-compose up
##### Эти команды создадут и запустят контейнеры для Django приложения и PostgreSQL базы данных.

Работа с Telegram ботом
1) Зайдите в Telegram и найдите своего бота. (не забудьте добавить телеграм апи токен)
2) Напишите боту команду /start и следуйте инструкциям для регистрации и настройки уведомлений.

Создание привычек
1) Получите токен аутентификации, отправив POST запрос на http://localhost:8000/users/token/ с вашими учетными данными.
2) В заголовке запроса укажите Authorization: Bearer <ваш_токен>.
3) Создайте новую привычку, отправив POST запрос на http://localhost:8000/habit/create/ с данными о привычке.