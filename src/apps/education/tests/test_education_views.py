import pytest
from django.urls import reverse

from apps.education.models import EducationSection, Education


@pytest.mark.django_db
class TestEducationViews:
    """
    Test suite for Education views.
    """

    # ------------------------------------------------
    # Education Section Add
    # ------------------------------------------------

    def test_add_section_get(self, client, user):
        url = reverse("education:add-section", args=[user.id])

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_add_section_post_success(self, client, user):
        url = reverse("education:add-section", args=[user.id])

        data = {
            "name": "Academic Background",
            "description": "My studies",
        }

        response = client.post(url, data)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"
        assert EducationSection.objects.filter(name="Academic Background").exists()

    def test_add_section_post_error(self, client, user):
        url = reverse("education:add-section", args=[user.id])

        response = client.post(url, {"name": ""})

        assert response.status_code == 200
        assert "form" in response.context

    # ------------------------------------------------
    # Education Section Update
    # ------------------------------------------------

    def test_update_section_get(self, client, education_section):
        url = reverse("education:update-section", args=[education_section.id])

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_update_section_post_success(self, client, education_section):
        url = reverse("education:update-section", args=[education_section.id])

        data = {
            "name": "Updated Section",
            "description": "Updated description",
        }

        response = client.post(url, data)

        education_section.refresh_from_db()

        assert response.status_code == 200
        assert education_section.name == "Updated Section"

    def test_update_section_post_error(self, client, education_section):
        url = reverse("education:update-section", args=[education_section.id])

        response = client.post(url, {"name": ""})

        assert response.status_code == 200
        assert "form" in response.context

    # ------------------------------------------------
    # Education Section Delete
    # ------------------------------------------------

    def test_delete_section_get(self, client, education_section):
        url = reverse("education:delete-section", args=[education_section.id])

        response = client.get(url)

        assert response.status_code == 200

    def test_delete_section_post(self, client, education_section):
        url = reverse("education:delete-section", args=[education_section.id])

        response = client.post(url)

        assert response.status_code == 200
        assert not EducationSection.objects.filter(id=education_section.id).exists()

    # ------------------------------------------------
    # Education Add
    # ------------------------------------------------

    def test_add_education_get(self, client, education_section):
        url = reverse("education:add", args=[education_section.id])

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_add_education_post_success(self, client, education_section):
        url = reverse("education:add", args=[education_section.id])

        data = {
            "school": "MIT",
            "degree": "Master",
            "field_of_study": "AI",
            "start_date": "2020-01-01",
            "end_date": "2022-01-01",
            "description": "Test",
        }

        response = client.post(url, data)

        assert response.status_code == 200
        assert Education.objects.filter(school="MIT").exists()

    def test_add_education_post_error(self, client, education_section):
        url = reverse("education:add", args=[education_section.id])

        response = client.post(url, {})

        assert response.status_code == 200
        assert "form" in response.context

    # ------------------------------------------------
    # Education Update
    # ------------------------------------------------

    def test_update_education_get(self, client, education_entry):
        url = reverse("education:update", args=[education_entry.id])

        response = client.get(url)

        assert response.status_code == 200

    def test_update_education_post_success(self, client, education_entry):
        url = reverse("education:update", args=[education_entry.id])

        data = {
            "education_section": education_entry.education_section.id,
            "school": "Updated University",
            "degree": "Updated Degree",
            "field_of_study": "AI",
            "start_date": "2020-01-01",
            "end_date": "2023-01-01",
            "description": "Updated",
        }

        response = client.post(url, data)

        education_entry.refresh_from_db()

        assert response.status_code == 200
        assert education_entry.school == "Updated University"

    # ------------------------------------------------
    # Education Delete
    # ------------------------------------------------

    def test_delete_education_get(self, client, education_entry):
        url = reverse("education:delete", args=[education_entry.id])

        response = client.get(url)

        assert response.status_code == 200

    def test_delete_education_post(self, client, education_entry):
        url = reverse("education:delete", args=[education_entry.id])

        response = client.post(url)

        assert response.status_code == 200
        assert not Education.objects.filter(id=education_entry.id).exists()
