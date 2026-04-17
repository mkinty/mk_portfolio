import pytest
from django.urls import reverse

from apps.techstack.models import TechStackCategory, TechStack


@pytest.mark.django_db
class TestTechStackCategoryAddView:

    def test_get(self, client, user):
        url = reverse("techstack:add-category", args=[user.id])
        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_post_success(self, client, user):
        url = reverse("techstack:add-category", args=[user.id])

        response = client.post(url, {
            "name": "Frontend",
            "order": 1
        })

        assert response.status_code == 200
        assert TechStackCategory.objects.count() == 1

    def test_post_invalid(self, client, user):
        url = reverse("techstack:add-category", args=[user.id])

        response = client.post(url, {
            "name": ""
        })

        assert response.status_code == 200
        assert "form" in response.context


@pytest.mark.django_db
class TestTechStackCategoryUpdateView:

    def test_get(self, client, tech_category):
        url = reverse("techstack:update-category", args=[tech_category.id])
        response = client.get(url)

        assert response.status_code == 200

    def test_post_success(self, client, tech_category):
        url = reverse("techstack:update-category", args=[tech_category.id])

        response = client.post(url, {
            "name": "Updated",
            "order": 2,
        })

        tech_category.refresh_from_db()

        assert response.status_code == 200
        assert tech_category.name == "Updated"


@pytest.mark.django_db
class TestTechStackCategoryDeleteView:

    def test_get(self, client, tech_category):
        url = reverse("techstack:delete-category", args=[tech_category.id])
        response = client.get(url)

        assert response.status_code == 200

    def test_post(self, client, tech_category):
        url = reverse("techstack:delete-category", args=[tech_category.id])

        response = client.post(url)

        assert response.status_code == 200
        assert TechStackCategory.objects.count() == 0


@pytest.mark.django_db
class TestTechStackAddView:

    def test_get(self, client, user):
        url = reverse("techstack:add", args=[user.id])
        response = client.get(url)

        assert response.status_code == 200

    def test_post_success(self, client, user, tech_category):
        url = reverse("techstack:add", args=[user.id])

        response = client.post(url, {
            "name": "Django",
            "category": tech_category.id
        })

        assert response.status_code == 200
        assert TechStack.objects.count() == 1

    def test_post_invalid(self, client, user):
        url = reverse("techstack:add", args=[user.id])

        response = client.post(url, {
            "name": ""
        })

        assert response.status_code == 200
        assert "form" in response.context


@pytest.mark.django_db
class TestTechStackUpdateView:

    def test_get(self, client, tech_stack):
        url = reverse("techstack:update", args=[tech_stack.id])
        response = client.get(url)

        assert response.status_code == 200

    def test_post(self, client, tech_stack, tech_category):
        url = reverse("techstack:update", args=[tech_stack.id])

        response = client.post(url, {
            "name": "FastAPI",
            "category": tech_category.id
        })

        tech_stack.refresh_from_db()

        assert response.status_code == 200
        assert tech_stack.name == "FastAPI"


@pytest.mark.django_db
class TestTechStackDeleteView:

    def test_get(self, client, tech_stack):
        url = reverse("techstack:delete", args=[tech_stack.id])
        response = client.get(url)

        assert response.status_code == 200

    def test_post(self, client, tech_stack):
        url = reverse("techstack:delete", args=[tech_stack.id])

        response = client.post(url)

        assert response.status_code == 200
        assert TechStack.objects.count() == 0
