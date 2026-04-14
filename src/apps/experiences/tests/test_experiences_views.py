import pytest
from django.urls import reverse

from apps.experiences.models import Experience

import pytest
from django.urls import reverse

from apps.experiences.models import Experience


@pytest.mark.django_db
class TestExperienceViews:
    """
    Test suite for Experience views.

    This class verifies the full CRUD lifecycle of Experience views:
    - Create (add)
    - Read (get form)
    - Update
    - Delete

    Coverage:
        - GET requests render correct templates and context
        - POST requests create/update/delete objects correctly
        - Form validation (success and failure cases)
        - HTMX response headers
        - Database state consistency
    """

    # =========================================================
    # CREATE (ADD EXPERIENCE)
    # =========================================================

    def test_add_get(self, client, user):
        """
        Ensure the add experience form is correctly rendered.

        Steps:
            1. Call GET add view
            2. Verify HTTP 200 response
            3. Verify form and user context exist
        """
        url = reverse("experiences:add", kwargs={"user_id": user.id})
        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["user_obj"] == user

    def test_add_post_success(self, client, user):
        """
        Ensure an experience is created successfully.

        Steps:
            1. Submit valid POST data
            2. Verify HTMX success response
            3. Verify object is created in database
        """
        url = reverse("experiences:add", kwargs={"user_id": user.id})

        data = {
            "title": "Dev",
            "company": "Company",
            "start_date": "2023-01-01",
        }

        response = client.post(url, data)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"
        assert Experience.objects.filter(user=user).exists()

    def test_add_post_failure(self, client, user):
        """
        Ensure invalid data does not create an experience.

        Steps:
            1. Submit invalid POST data
            2. Verify form is returned with errors
            3. Verify no object is created
        """
        url = reverse("experiences:add", kwargs={"user_id": user.id})

        data = {
            "title": "",  # invalid field
        }

        response = client.post(url, data)

        assert response.status_code == 200
        assert "form" in response.context
        assert Experience.objects.filter(user=user).count() == 0

    # =========================================================
    # UPDATE EXPERIENCE
    # =========================================================

    def test_update_get(self, client, experience):
        """
        Ensure update form is rendered with existing data.

        Steps:
            1. Call GET update view
            2. Verify HTTP 200 response
            3. Verify experience is in context
        """
        url = reverse("experiences:update", kwargs={"experience_id": experience.id})
        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["experience"] == experience

    def test_update_post_success(self, client, experience):
        """
        Ensure an experience is successfully updated.

        Steps:
            1. Submit valid update data
            2. Verify HTMX success response
            3. Verify database is updated
        """
        url = reverse("experiences:update", kwargs={"experience_id": experience.id})

        data = {
            "title": "Updated title",
            "company": experience.company,
            "start_date": "2023-01-01",
        }

        response = client.post(url, data)

        experience.refresh_from_db()

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"
        assert experience.title == "Updated title"

    def test_update_post_failure(self, client, experience):
        """
        Ensure invalid update data does not modify object.

        Steps:
            1. Submit invalid data
            2. Verify form errors are returned
        """
        url = reverse("experiences:update", kwargs={"experience_id": experience.id})

        data = {
            "title": "",  # invalid
        }

        response = client.post(url, data)

        assert response.status_code == 200
        assert "form" in response.context

    # =========================================================
    # DELETE EXPERIENCE
    # =========================================================

    def test_delete_get(self, client, experience):
        """
        Ensure delete confirmation page is displayed.

        Steps:
            1. Call GET delete view
            2. Verify HTTP 200 response
            3. Verify experience is in context
        """
        url = reverse("experiences:delete", kwargs={"experience_id": experience.id})
        response = client.get(url)

        assert response.status_code == 200
        assert "experience" in response.context

    def test_delete_post(self, client, experience):
        """
        Ensure experience is deleted successfully.

        Steps:
            1. Call POST delete view
            2. Verify HTMX success response
            3. Verify object is removed from database
        """
        url = reverse("experiences:delete", kwargs={"experience_id": experience.id})

        response = client.post(url)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"
        assert not Experience.objects.filter(id=experience.id).exists()
