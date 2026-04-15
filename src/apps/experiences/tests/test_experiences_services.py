import pytest

from apps.experiences.models import Experience
from apps.experiences.services.experiences_services import ExperienceService


@pytest.mark.django_db
class TestExperienceService:
    """
    Test suite for ExperienceService class.
    """

    def test_get_add_form(self, user):
        """
        Test retrieving an empty experience form with user.
        """
        form, returned_user = ExperienceService.get_add_form(user.pk)

        assert returned_user == user
        assert form is not None

    def test_create_experience_success(self, user):
        """
        Test successful creation of an experience.
        """
        data = {
            "title": "Backend Developer",
            "company": "OpenAI",
            "start_date": "2023-01-01",
            "is_current": True,
            "description": "Building APIs",
        }

        success, form, experience = ExperienceService.create(
            user=user,
            data=data,
            files=None
        )

        assert success is True
        assert experience is not None
        assert isinstance(experience, Experience)
        assert experience.user == user
        assert experience.company == "OpenAI"

    def test_create_experience_failure(self, user):
        """
        Test creation failure when data is invalid.
        """
        data = {
            "company": "OpenAI",  # missing required fields
        }

        success, form, experience = ExperienceService.create(
            user=user,
            data=data,
            files=None
        )

        assert success is False
        assert experience is None
        assert form.errors

    def test_get_update_form(self, experience):
        """
        Test retrieving update form for an experience.
        """
        form, exp = ExperienceService.get_update_form(experience.id)

        assert exp == experience
        assert form.instance == experience

    def test_update_experience_success(self, experience):
        """
        Test successful update of an experience.
        """
        data = {
            "title": "Updated Title",
            "company": "Updated Company",
            "start_date": "2023-01-01",
            "is_current": False,
            "description": "Updated description",
        }

        success, form, updated_exp = ExperienceService.update(
            experience_id=experience.id,
            data=data,
            files=None
        )

        updated_exp.refresh_from_db()

        assert success is True
        assert updated_exp.title == "Updated Title"
        assert updated_exp.company == "Updated Company"

    def test_update_experience_invalid(self, experience):
        """
        Test update failure with invalid data.
        """
        data = {
            "title": "",  # invalid
        }

        success, form, exp = ExperienceService.update(
            experience_id=experience.id,
            data=data,
            files=None
        )

        assert success is False
        assert form.errors

    def test_delete_experience(self, experience):
        """
        Test deletion of an experience.
        """
        exp_id = experience.id

        ExperienceService.delete(experience.id)

        assert Experience.objects.filter(id=exp_id).exists() is False
