import pytest

from apps.experiences.models import Experience
from apps.experiences.selectors.experiences_selectors import get_experience_by_id, get_all_experiences


@pytest.mark.django_db
class TestExperienceSelectors:
    """
    Test suite for get_experience_by_id selector.
    """

    def test_get_existing_experience(self, experience):
        """
        Should return an Experience instance when ID exists.
        """
        result = get_experience_by_id(experience.id)

        assert result is not None
        assert isinstance(result, Experience)
        assert result.id == experience.id
        assert result.title == experience.title

    def test_get_non_existing_experience(self):
        """
        Should return None when experience does not exist.
        """
        result = get_experience_by_id(999999)

        assert result is None

    def test_get_experience_by_id_with_fixture_data(self, experience, user):
        """
        Should correctly retrieve fixture experience.
        """
        result = get_experience_by_id(experience.id)

        assert result.user == user
        assert result.company == "Test Company"

    def test_get_all_experiences(self, experience):
        """
        Should return a list of all experiences.
        """
        result = get_all_experiences(experience.user)

        assert len(result) == 1
        assert result[0].id == experience.id
        assert result[0].title == experience.title
        assert result[0].company == "Test Company"
        assert result[0].user == experience.user