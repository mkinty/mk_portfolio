import pytest
from apps.userprofile.selectors.userprofile_selectors import (
    get_userprofile_by_id,
    get_userprofile_by_user
)


@pytest.mark.django_db
def test_get_userprofile_by_id_returns_profile(user_profile):
    """ Test that get_userprofile_by_id returns the correct profile """
    assert get_userprofile_by_id(user_profile.id) == user_profile


@pytest.mark.django_db
def test_get_userprofile_by_id_returns_none():
    """ Test that get_userprofile_by_id returns None for non-existent ID """
    assert get_userprofile_by_id(999999) is None


@pytest.mark.django_db
def test_get_userprofile_by_user_returns_profile(user, user_profile):
    """ Test that get_userprofile_by_user returns the correct profile """
    assert get_userprofile_by_user(user) == user_profile


@pytest.mark.django_db
def test_get_userprofile_by_user_returns_none(user):
    """ Test that get_userprofile_by_user returns None when profile is deleted """
    user.profile.delete()
    assert get_userprofile_by_user(user) is None


@pytest.mark.django_db
def test_get_userprofile_by_user_with_none():
    """ Test that get_userprofile_by_user returns None when user is None """
    assert get_userprofile_by_user(None) is None
