import pytest

from apps.skills.services.skills_servives import SkillsService


@pytest.mark.django_db
class TestSkillsServices:
    """
    Test suite for SkillsService
    """

    def test_get_add_form(self, user):
        """
        Test getting the add form
        """
        form, returned_user = SkillsService.get_add_form(user.pk)
        assert form is not None
        assert returned_user == user

    def test_create_skill_success(self, user):
        """
        Test creating a skill successfully
        """
        data = {
            "name": "Technical skills",
            "description": "Technical skills description",
        }
        success, form, skill = SkillsService.create(user=user, data=data, files=None)

        assert success is True
        assert form is not None
        assert skill is not None
        assert skill.name == "Technical skills"
        assert skill.description == "Technical skills description"

    def test_create_skill_failure(self, user):
        """
        Test creating a skill with invalid data
        """
        data = {
            "name": "",
            "description": "",
        }
        success, form, skill = SkillsService.create(user=user, data=data, files=None)

        assert success is False
        assert form.errors
        assert skill is None

    def test_get_update_form(self, skill):
        """Tes retrieving update form for a skill"""
        form, returned_skill = SkillsService.get_update_form(skill_id=skill.id)
        assert form is not None
        assert form.instance == skill

    def test_update_skill_success(self, skill):
        """
        Test updating a skill successfully
        """
        data = {
            "name": "Updated Technical skills",
            "description": "Updated Technical skills description",
        }

        success, form, updated_skill = SkillsService.update(
            skill_id=skill.id,
            data=data,
            files={},  # FIX
        )

        updated_skill.refresh_from_db()

        assert success is True
        assert form is not None
        assert updated_skill is not None
        assert updated_skill.name == "Updated Technical skills"
        assert updated_skill.description == "Updated Technical skills description"

    def test_update_skill_failure(self, skill):
        """
        Test updating a skill with invalid data
        """
        data = {
            "name": "",
            "description": "",
        }
        success, form, updated_skill = SkillsService.update(
            skill_id=skill.id,
            data=data,
            files=None,
        )

        updated_skill.refresh_from_db()

        assert success is False
        assert form.errors
        assert updated_skill is not None
        assert updated_skill.name == skill.name
        assert updated_skill.description == skill.description

    def test_delete_skill(self, skill):
        """
        Test deleting a skill
        """
        success = SkillsService.delete(skill.id)

        assert success is True
        with pytest.raises(skill.DoesNotExist):
            skill.refresh_from_db()
