from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Ad
from .serializers import AdSerializer


class AdViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений."""

    serializer_class = AdSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    def get_queryset(self):
        """Базовый queryset — все объявления."""
        return Ad.objects.select_related("author").all()

    def list(self, request, *args, **kwargs):
        """Список объявлений с фильтрацией."""
        queryset = self.get_queryset()

        # Фильтр по статусу (по умолчанию published)
        status_param = request.query_params.get("status", "published")
        queryset = queryset.filter(status=status_param)

        # Поиск по заголовку (без учёта регистра)
        search_param = request.query_params.get("search")
        if search_param:
            queryset = queryset.filter(title__icontains=search_param)

        # Сортировка: новые первыми, при совпадении даты — по id по убыванию
        queryset = queryset.order_by("-created_at", "-id")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Получение объявления по id (любой статус)."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Создание объявления."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """Частичное обновление объявления."""
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Удаление объявления."""
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
