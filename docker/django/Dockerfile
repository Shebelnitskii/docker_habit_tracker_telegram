# Используйте базовый образ Python
FROM python:3

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Копируйте зависимости проекта
COPY ./requirements.txt .

# Установите зависимости
RUN pip install -r requirements.txt

# Копируйте весь проект внутрь контейнера
COPY . .

CMD ["python", "manage.py", "migrate"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]