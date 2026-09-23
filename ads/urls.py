from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdViewSet

# Создаём роутер и регистрируем ViewSet
router = DefaultRouter()
router.register(r"ads", AdViewSet, basename="ad")

urlpatterns = [
    # Подключаем все маршруты из роутера
    path("", include(router.urls)),
]
