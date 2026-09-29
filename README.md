# Ylab Ads API

REST API для сервиса объявлений (тестовое задание стажировки Ylab).

## Требования

- Python 3.12+
- Docker и Docker Compose
- PostgreSQL (для локальной разработки)

## Установка и запуск

### Через Docker Compose (рекомендуется)

docker compose up --build

API будет доступно на <http://localhost:8000/api/ads/>

### Локальная разработка

### 1. Создайте базу данных PostgreSQL

sudo -u postgres psql -c "CREATE DATABASE ylab_ads;"

### 2. Установите зависимости

Современный способ установки зависимостей:

uv sync

Альтернативный способ установки зависимостей:

uv pip install -r requirements.txt

### 3. Примените миграции

python manage.py migrate
python manage.py loaddata authors

### 4. Запустите сервер

python manage.py runserver

## API Endpoints

- POST /api/ads/ — Создать объявление
- GET /api/ads/ — Список объявлений (фильтры: status, search)
- GET /api/ads/{id}/ — Получить объявление
- PATCH /api/ads/{id}/ — Обновить объявление
- DELETE /api/ads/{id}/ — Удалить объявление

## Тесты

pytest -v

## Структура проекта

- ads/ — приложение с моделями, views и serializers
- config/ — настройки Django проекта
- fixtures/ — тестовые данные (авторы)
- Dockerfile, docker-compose.yaml — контейнеризация
- pyproject.toml, uv.lock — зависимости (uv)
- .pre-commit-config.yaml — pre-commit хуки (Ruff)

## Технологии

- Django 6.1
- Django REST Framework
- PostgreSQL
- Docker
- uv (менеджер зависимостей)
- pytest (тестирование)
