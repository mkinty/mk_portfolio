import pytest

from apps.userprofile.selectors.userprofile_selectors import (
    get_userprofile_by_id,
    get_userprofile_by_user
)


@pytest.mark.django_db
class TestUserProfileSelectors:
    """
    Test suite for UserProfile selectors.
    """

    def test_get_userprofile_by_id_returns_profile(self, user_profile):
        """
        Test that get_userprofile_by_id returns the correct profile.
        """
        result = get_userprofile_by_id(user_profile.id)

        assert result == user_profile

    def test_get_userprofile_by_id_returns_none(self):
        """
        Test that get_userprofile_by_id returns None for non-existent ID.
        """
        result = get_userprofile_by_id(999999)

        assert result is None

    def test_get_userprofile_by_user_returns_profile(self, user, user_profile):
        """
        Test that get_userprofile_by_user returns the correct profile.
        """
        result = get_userprofile_by_user(user)

        assert result == user_profile

    def test_get_userprofile_by_user_returns_none(self, user):
        """
        Test that get_userprofile_by_user returns None when profile is deleted.
        """
        user.profile.delete()

        result = get_userprofile_by_user(user)

        assert result is None

    def test_get_userprofile_by_user_with_none(self):
        """
        Test that get_userprofile_by_user returns None when user is None.
        """
        result = get_userprofile_by_user(None)

        assert result is None
