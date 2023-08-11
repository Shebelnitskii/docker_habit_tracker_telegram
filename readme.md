Проект "Shebelnitskiy Habit Tracker" представляет собой веб-приложение для отслеживания привычек через Telegram бота.

Установка
Клонируйте репозиторий на свой компьютер:
- git clone https://github.com/Shebelnitskii/course_work_drf.git

Перейдите в директорию проекта:
- cd course_work_drf

Создайте и активируйте виртуальное окружение:
- python -m venv venv
- source venv/bin/activate

Установите зависимости из файла requirements.txt:
- pip install -r requirements.txt

Настройка:
- Создайте файл .env в корневой директории проекта и скопируйте в него содержимое из .env.sample. Заполните необходимые параметры, такие как TELEGRAM_API_TOKEN, DB_NAME, DB_USER, DB_PASSWORD настройки подключения к базе данных и другие.

Запуск:
1) Запустите сервер Django:
    - python manage.py runserver
2) Запустите Celery worker для обработки задач:
    - celery -A config worker -l info
3) Запустите Celery beat для планирования задач:
    - celery -A config beat -l info
4) Откройте браузер и перейдите по адресу http://localhost:8000/ для проверки работоспособности сервера.

Работа с Telegram ботом
1) Зайдите в Telegram и найдите бота @shebelnitskiy_habit_bot.
2) Напишите боту команду /start и следуйте инструкциям для регистрации и настройки уведомлений.

Создание привычек
1) Получите токен аутентификации, отправив POST запрос на http://localhost:8000/users/token/ с вашими учетными данными.
2) В заголовке запроса укажите Authorization: Bearer <ваш_токен>.
3) Создайте новую привычку, отправив POST запрос на http://localhost:8000/habit/create/ с данными о привычке.