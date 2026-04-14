import pytest
from datetime import date

from apps.experiences.models import Experience


@pytest.mark.django_db
class TestExperienceModel:
    """
    Test suite for the Experience model.
    """

    def test_experience_fixture(self, experience):
        """
        Test experience fixture values.
        """
        assert experience.title == "Test Experience"
        assert experience.company == "Test Company"
        assert experience.is_current is False

    def test_str_representation(self, experience):
        """
        Test string representation.
        """
        assert str(experience) == "Test Experience - Test Company"

    def test_user_relation(self, user, experience):
        """
        Test relation between user and experience.
        """
        assert experience.user == user
        assert experience in user.experiences.all()

    def test_create_new_experience(self, user):
        """
        Test creating a new experience instance.
        """
        experience = Experience.objects.create(
            user=user,
            title="Senior Developer",
            company="Google",
            start_date=date(2022, 1, 1),
            is_current=True
        )

        assert experience.title == "Senior Developer"
        assert experience.is_current is True

    def test_optional_fields(self, experience):
        """
        Test default values for optional fields.
        """
        assert experience.location == ""
        assert experience.end_date is None
