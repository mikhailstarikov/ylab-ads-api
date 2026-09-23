import pytest
from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup():
    """Настройка тестовой базы данных."""
    pass


@pytest.fixture
def author(db):
    """Фикстура автора."""
    from ads.models import Author

    return Author.objects.create(name="Тестовый Автор")


@pytest.fixture
def ad(db, author):
    """Фикстура объявления."""
    from ads.models import Ad

    return Ad.objects.create(
        title="Тестовое объявление",
        description="Описание тестового объявления",
        price=1000.00,
        status="draft",
        author=author,
    )


@pytest.fixture
def published_ad(db, author):
    """Фикстура опубликованного объявления."""
    from ads.models import Ad

    return Ad.objects.create(
        title="Опубликованное объявление",
        description="Описание опубликованного объявления",
        price=2000.00,
        status="published",
        author=author,
    )
