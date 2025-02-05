# Используем официальный образ Python (например, slim-версию)
FROM python:3.10-slim

# Задаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями в контейнер
COPY requirements.txt /app/requirements.txt

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . /app

# Открываем порт 8000 для доступа к серверу
EXPOSE 8000

# По умолчанию запускаем сервер Django (можно изменить на runbot, если нужно)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
