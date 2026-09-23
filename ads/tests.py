import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ads.models import Author, Ad


@pytest.fixture
def api_client():
    """Фикстура API клиента."""
    return APIClient()


@pytest.mark.django_db
class TestAdCreation:
    """Тесты создания и обновления объявлений."""

    def test_create_ad_success(self, api_client, author):
        """Успешное создание объявления."""
        url = reverse("ad-list")
        data = {
            "title": "Новое объявление",
            "description": "Описание нового объявления",
            "price": 5000.00,
            "author_id": author.id,
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == data["title"]
        assert response.data["status"] == "draft"
        assert "id" in response.data
        assert "created_at" in response.data

    def test_create_ad_default_status_draft(self, api_client, author):
        """Статус по умолчанию — draft."""
        url = reverse("ad-list")
        data = {
            "title": "Объявление без статуса",
            "description": "Описание",
            "price": 1000.00,
            "author_id": author.id,
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "draft"

    def test_partial_update_ad(self, api_client, ad):
        """Частичное обновление объявления."""
        url = reverse("ad-detail", kwargs={"pk": ad.id})
        data = {"title": "Обновлённый заголовок"}
        response = api_client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == data["title"]
        assert response.data["description"] == ad.description
        assert Decimal(response.data["price"]) == ad.price


@pytest.mark.django_db
class TestAdRetrieval:
    """Тесты получения и удаления объявлений."""

    def test_get_ad_success(self, api_client, ad):
        """Успешное получение объявления."""
        url = reverse("ad-detail", kwargs={"pk": ad.id})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == ad.id
        assert "author" in response.data
        assert response.data["author"]["name"] == ad.author.name

    def test_get_ad_not_found(self, api_client):
        """Получение несуществующего объявления — 404."""
        url = reverse("ad-detail", kwargs={"pk": 9999})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_ad_success(self, api_client, ad):
        """Успешное удаление объявления."""
        url = reverse("ad-detail", kwargs={"pk": ad.id})
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Ad.objects.filter(id=ad.id).exists()

    def test_get_deleted_ad_returns_404(self, api_client, ad):
        """Получение удалённого объявления — 404."""
        url = reverse("ad-detail", kwargs={"pk": ad.id})
        api_client.delete(url)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestAdValidation:
    """Тесты валидации."""

    def test_create_ad_missing_required_fields(self, api_client, author):
        """Создание без обязательных полей — ошибка."""
        url = reverse("ad-list")
        data = {"author_id": author.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data
        assert "description" in response.data
        assert "price" in response.data

    def test_create_ad_invalid_price_negative(self, api_client, author):
        """Отрицательная цена — ошибка."""
        url = reverse("ad-list")
        data = {
            "title": "Объявление",
            "description": "Описание",
            "price": -100.00,
            "author_id": author.id,
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "price" in response.data

    def test_create_ad_invalid_status(self, api_client, author):
        """Недопустимый статус — ошибка."""
        url = reverse("ad-list")
        data = {
            "title": "Объявление",
            "description": "Описание",
            "price": 1000.00,
            "author_id": author.id,
            "status": "invalid_status",
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "status" in response.data

    def test_create_ad_empty_title_whitespace(self, api_client, author):
        """Заголовок из пробелов — ошибка."""
        url = reverse("ad-list")
        data = {"title": "   ", "description": "Описание", "price": 1000.00, "author_id": author.id}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestAdListFiltering:
    """Тесты фильтрации и поиска."""

    def test_list_ads_default_published_only(self, api_client, author):
        """По умолчанию показываются только published."""
        Ad.objects.all().delete()
        Ad.objects.create(
            title="Черновик",
            description="Описание черновика",
            price=1000.00,
            status="draft",
            author=author,
        )
        published_ad = Ad.objects.create(
            title="Опубликовано",
            description="Описание опубликованного",
            price=2000.00,
            status="published",
            author=author,
        )

        url = reverse("ad-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["id"] == published_ad.id

    def test_list_ads_filter_by_status(self, api_client, author):
        """Фильтр по статусу."""
        Ad.objects.all().delete()
        draft_ad = Ad.objects.create(
            title="Черновик",
            description="Описание черновика",
            price=1000.00,
            status="draft",
            author=author,
        )
        Ad.objects.create(
            title="Опубликовано",
            description="Описание опубликованного",
            price=2000.00,
            status="published",
            author=author,
        )

        url = reverse("ad-list") + "?status=draft"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["id"] == draft_ad.id

    def test_list_ads_search_by_title(self, api_client, author):
        """Поиск по заголовку (без учёта регистра)."""
        Ad.objects.all().delete()
        Ad.objects.create(
            title="iPhone 15 Pro",
            description="Новый iPhone",
            price=100000.00,
            status="published",
            author=author,
        )
        Ad.objects.create(
            title="Samsung Galaxy",
            description="Samsung",
            price=80000.00,
            status="published",
            author=author,
        )

        url = reverse("ad-list") + "?search=iphone"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert "iPhone" in response.data["results"][0]["title"]

    def test_list_ads_combined_filters(self, api_client, author):
        """Сочетание фильтра и поиска."""
        Ad.objects.all().delete()
        Ad.objects.create(
            title="MacBook Pro",
            description="MacBook",
            price=150000.00,
            status="published",
            author=author,
        )
        Ad.objects.create(
            title="MacBook Air",
            description="MacBook Air",
            price=100000.00,
            status="draft",
            author=author,
        )

        url = reverse("ad-list") + "?status=published&search=macbook"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert "MacBook Pro" in response.data["results"][0]["title"]

    def test_list_ads_sorting_newest_first(self, api_client, author):
        """Сортировка: новые первыми, при совпадении даты — по id по убыванию."""
        Ad.objects.all().delete()
        import time

        ad1 = Ad.objects.create(
            title="Первое",
            description="Описание 1",
            price=1000.00,
            status="published",
            author=author,
        )
        time.sleep(0.01)
        ad2 = Ad.objects.create(
            title="Второе",
            description="Описание 2",
            price=2000.00,
            status="published",
            author=author,
        )

        url = reverse("ad-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["id"] == ad2.id
        assert response.data["results"][1]["id"] == ad1.id

    def test_publish_via_patch(self, api_client, author):
        """Публикация через PATCH."""
        Ad.objects.all().delete()
        ad = Ad.objects.create(
            title="Черновик для публикации",
            description="Описание",
            price=1000.00,
            status="draft",
            author=author,
        )

        url = reverse("ad-detail", kwargs={"pk": ad.id})
        data = {"status": "published"}
        response = api_client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "published"

        list_url = reverse("ad-list")
        list_response = api_client.get(list_url)
        assert list_response.status_code == status.HTTP_200_OK
        assert any(item["id"] == ad.id for item in list_response.data["results"])
