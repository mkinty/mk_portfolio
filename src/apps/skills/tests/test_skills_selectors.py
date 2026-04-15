import pytest

from apps.skills.selectors.skills_selectors import SkillsSelectors


@pytest.mark.django_db
class TestSkillsSelectors:

    def test_get_existing_skill(self, skill):
        """
        Test retrieving an existing skill by ID.
        """
        result = SkillsSelectors.get_skill_by_id(skill.id)
        assert result is not None
        assert result == skill

    def test_get_non_existing_skill(self):
        """
        Test retrieving a non-existing skill by ID.
        """
        result = SkillsSelectors.get_skill_by_id(99999)
        assert result is None


    def test_get_all_skills(self, skill):
        """
        Test retrieving all skills for a user.
        """
        result = SkillsSelectors.get_all_skills(skill.user)
        assert len(result) == 1
        assert result[0] == skill