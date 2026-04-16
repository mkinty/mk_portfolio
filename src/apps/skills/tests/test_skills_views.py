import pytest
from django.urls import reverse

from apps.experiences.models import Experience
from apps.skills.models import Skills


@pytest.mark.django_db
class TestSkillsViews:
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
    # CREATE (ADD SKILL)
    # =========================================================

    def test_add_get(self, client, user):
        """
        Ensure the add skill form is correctly rendered.

        Steps:
            1. Call GET add view
            2. Verify HTTP 200 response
            3. Verify form and user context exist
        """
        url = reverse("skills:add", kwargs={"user_id": user.id})
        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["user_obj"] == user

    def test_add_post_success(self, client, user):
        """
        Ensure a skill is created successfully.

        Steps:
            1. Submit valid POST data
            2. Verify HTMX success response
            3. Verify object is created in database
        """
        url = reverse("skills:add", kwargs={"user_id": user.id})

        data = {
            "name": "Technical skills",
            "description": "Technical skills description",
        }

        response = client.post(url, data)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"
        assert Skills.objects.filter(user=user).exists()

    def test_add_post_failure(self, client, user):
        """
        Ensure invalid data does not create a skill.

        Steps:
            1. Submit invalid POST data
            2. Verify form is returned with errors
            3. Verify no object is created
        """
        url = reverse("skills:add", kwargs={"user_id": user.id})

        data = {
            "name": "",  # invalid field
        }

        response = client.post(url, data)

        assert response.status_code == 200
        assert "form" in response.context
        assert Skills.objects.filter(user=user).count() == 0

    # =========================================================
    # UPDATE SKILL
    # =========================================================

    def test_update_get(self, client, skill):
        """
        Ensure update form is rendered with existing data.

        Steps:
            1. Call GET update view
            2. Verify HTTP 200 response
            3. Verify skill is in context
        """
        url = reverse("skills:update", kwargs={"skill_id": skill.id})
        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["skill"] == skill

    def test_update_post_success(self, client, skill):
        """
        Ensure a skill is successfully updated.

        Steps:
            1. Submit valid update data
            2. Verify HTMX success response
            3. Verify database is updated
        """
        url = reverse("skills:update", kwargs={"skill_id": skill.id})


        data = {
            "name": "Updated Technical skills",
            "description": "Updated Technical skills description",
        }

        response = client.post(url, data)

        skill.refresh_from_db()

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"
        assert skill.name == "Updated Technical skills"

    def test_update_post_failure(self, client, skill):
        """
        Ensure invalid update data does not modify object.

        Steps:
            1. Submit invalid data
            2. Verify form errors are returned
        """
        url = reverse("skills:update", kwargs={"skill_id": skill.id})

        data = {
            "name": "",  # invalid
        }

        response = client.post(url, data)

        assert response.status_code == 200
        assert "form" in response.context

    # =========================================================
    # DELETE SKILL
    # =========================================================

    def test_delete_get(self, client, skill):
        """
        Ensure delete confirmation page is displayed.

        Steps:
            1. Call GET delete view
            2. Verify HTTP 200 response
            3. Verify experience is in context
        """
        url = reverse("skills:delete", kwargs={"skill_id": skill.id})
        response = client.get(url)

        assert response.status_code == 200
        assert "skill" in response.context

    def test_delete_post(self, client, skill):
        """
        Ensure skill is deleted successfully.

        Steps:
            1. Call POST delete view
            2. Verify HTMX success response
            3. Verify object is removed from database
        """
        url = reverse("skills:delete", kwargs={"skill_id": skill.id})

        response = client.post(url)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"
        assert not Skills.objects.filter(id=skill.id).exists()
