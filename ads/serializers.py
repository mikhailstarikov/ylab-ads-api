from rest_framework import serializers
from .models import Author, Ad


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для автора - только чтение."""

    class Meta:
        model = Author
        fields = ["id", "name"]
        read_only_fields = fields


class AdSerializer(serializers.ModelSerializer):
    """Сериализатор для объявления."""

    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author", write_only=True, required=False
    )

    class Meta:
        model = Ad
        fields = [
            "id",
            "title",
            "description",
            "price",
            "status",
            "author",
            "author_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "author"]

    def validate_title(self, value):
        """Проверка заголовка - не пустая строка."""
        if not value or not value.strip():
            raise serializers.ValidationError("Заголовок не может быть пустым")
        return value.strip()

    def validate_description(self, value):
        """Проверка описания - не пустая строка."""
        if not value or not value.strip():
            raise serializers.ValidationError("Описание не может быть пустым")
        return value.strip()

    def validate_price(self, value):
        """Проверка цены - неотрицательное число."""
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной")
        return value

    def validate_status(self, value):
        """Проверка статуса - только допустимые значения."""
        valid_statuses = [choice[0] for choice in Ad.Status.choices]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Недопустимый статус. Доступные значения: {', '.join(valid_statuses)}"
            )
        return value
