FROM python:3.12-slim

# Устанавливаем uv
RUN pip install uv

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости через uv
RUN uv pip install --system -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт
EXPOSE 8000

# Запускаем миграции, фикстуры и сервер
CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata authors && python manage.py runserver 0.0.0.0:8000"]