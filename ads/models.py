from django.db import models


class Author(models.Model):
    """Модель автора объявлений."""

    name = models.CharField(
        max_length=120,
        verbose_name="Имя автора",
        help_text="Непустая строка до 120 символов",
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Ad(models.Model):
    """Модель объявления."""

    class Status(models.TextChoices):
        """Доступные статусы объявления."""

        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Опубликовано"
        ARCHIVED = "archived", "В архиве"

    title = models.CharField(
        max_length=120,
        verbose_name="Заголовок",
        help_text="Непустая строка до 120 символов",
    )
    description = models.TextField(
        max_length=5000,
        verbose_name="Описание",
        help_text="Непустая строка до 5000 символов",
    )
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Цена в рублях от 0 до 999999999.99",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Статус",
        help_text="draft/published/archived",
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="ads",
        verbose_name="Автор",
        help_text="Связь с автором объявления",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
