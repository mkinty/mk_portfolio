import pytest
from apps.userprofile.forms import UserProfileForm
from apps.userprofile.services.userprofile_services import (
    get_userprofile_add_form,
    create_userprofile,
    get_userprofile_update_form,
    update_userprofile,
    delete_user_profile,
)


@pytest.mark.django_db
def test_get_userprofile_add_form(user):
    """
    Test that get_userprofile_add_form returns a UserProfileForm and the associated user.
    """
    form, returned_user = get_userprofile_add_form(user.id)

    assert isinstance(form, UserProfileForm)
    assert returned_user == user


@pytest.mark.django_db
def test_create_userprofile_success(user):
    """ Test that create_userprofile creates a new user profile successfully """
    user.profile.delete()

    data = {
        'bio': "Test bio"
    }

    success, form, userprofile = create_userprofile(user, data, {})

    assert success is True
    assert form is not None
    assert userprofile.user == user


@pytest.mark.django_db
def test_get_userprofile_update_form(user_profile):
    """ Test that get_userprofile_update_form returns a UserProfileForm and the associated user profile """
    form, userprofile = get_userprofile_update_form(user_profile.id)

    assert form.instance == user_profile
    assert userprofile == user_profile


@pytest.mark.django_db
def test_update_userprofile_success(user_profile):
    """ Test that update_userprofile updates the user profile successfully """
    data = {
        'bio': "Updated bio"
    }

    success, form, userprofile = update_userprofile(user_profile.id, data, {})

    assert success is True
    assert form is not None
    assert userprofile.bio == "Updated bio"


@pytest.mark.django_db
def test_delete_user_profile(user_profile):
    """ Test that delete_user_profile deletes the user profile """
    delete_user_profile(user_profile)

    from apps.userprofile.models import UserProfile

    assert not UserProfile.objects.filter(id=user_profile.id).exists()
