import pytest

from apps.skills.models import Skills


@pytest.mark.django_db
class TestSkillModel:
    """
    Test suite for the Skill model.
    """

    def test_skill_fixture(self, skill):
        """
        Test that the skill fixture is working correctly.
        """
        assert skill.name == "Test Skill"
        assert skill.description == "Test Description"
        assert skill.user.email == "test@example.com"

    def test_skill_str_representation(self, skill):
        """
        Test that the string representation of a skill is correct.
        """
        assert str(skill) == "Test Skill"

    def test_skill_user_relationship(self, skill):
        """
        Test that the skill is properly related to a user.
        """
        assert skill.user.email == "test@example.com"
        assert skill.user.first_name == "Test"
        assert skill.user.last_name == "User"

    def test_create_new_skill(self, user):
        """
        Test that a new skill can be created.
        """
        skill = Skills.objects.create(
            user=user, name="New Skill", description="New Description"
        )
        assert skill.name == "New Skill"
        assert skill.description == "New Description"
        assert skill.user.email == "test@example.com"

    def test_skill_max_length(self, skill):
        """
        Test that the skill name has a maximum length of 150 characters.
        """
        assert len(skill.name) <= 150
