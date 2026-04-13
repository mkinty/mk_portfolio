import pytest
from apps.userprofile.models import UserProfile


@pytest.mark.django_db
def test_userprofile_str(user_profile):
    """ Test that the string representation of the user profile is correct """
    assert str(user_profile) == f"Profil de {user_profile.user}"


@pytest.mark.django_db
def test_userprofile_user_relation(user, user_profile):
    """ Test that the user profile is related to the user """
    assert user_profile.user == user


@pytest.mark.django_db
def test_user_has_profile(user, user_profile):
    """ Test that the user has a profile """
    assert user.profile == user_profile


@pytest.mark.django_db
def test_userprofile_deleted_when_user_deleted(user):
    """ Test that the user profile is deleted when the user is deleted """
    profile = user.profile
    user.delete()
    assert not UserProfile.objects.filter(id=profile.id).exists()


@pytest.mark.django_db
def test_userprofile_optional_fields(user):
    """ Test that the user profile optional fields are empty by default """
    profile = user.profile
    assert profile.title == ""
    assert profile.position == ""
    assert profile.bio == ""
