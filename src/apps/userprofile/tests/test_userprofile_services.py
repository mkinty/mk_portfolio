import pytest

from apps.userprofile.models import UserProfile
from apps.userprofile.services.userprofile_services import UserProfileService


@pytest.mark.django_db
class TestUserProfileService:
    """
    Test suite for UserProfileService class.
    """

    def test_get_add_form(self, user):
        """
        Test retrieving empty form and user.
        """
        form, returned_user = UserProfileService.get_add_form(user.id)

        assert returned_user == user
        assert form is not None

    def test_create_userprofile_success(self, user):
        """
        Test successful creation of a user profile.
        """
        user.profile.delete()

        data = {
            "title": "Developer",
            "position": "Backend Engineer",
            "bio": "Some bio text",
        }

        success, form, profile = UserProfileService.create(
            user=user,
            data=data,
            files=None
        )

        assert success is True
        assert profile is not None
        assert isinstance(profile, UserProfile)
        assert profile.user == user
        assert profile.title == "Developer"

    def test_get_update_form(self, user_profile):
        """
        Test retrieving update form for existing profile.
        """
        form, profile = UserProfileService.get_update_form(user_profile.id)

        assert profile == user_profile
        assert form.instance == user_profile

    def test_update_userprofile_success(self, user_profile):
        """
        Test successful update of user profile.
        """
        data = {
            "title": "Updated Title",
            "position": "Updated Position",
            "bio": "Updated bio",
        }

        success, form, updated_profile = UserProfileService.update(
            userprofile_id=user_profile.id,
            data=data,
            files=None
        )

        updated_profile.refresh_from_db()

        assert success is True
        assert updated_profile.title == "Updated Title"
        assert updated_profile.position == "Updated Position"

    def test_delete_userprofile(self, user_profile):
        """
        Test deletion of user profile.
        """
        profile_id = user_profile.id

        UserProfileService.delete(user_profile)

        assert UserProfile.objects.filter(id=profile_id).exists() is False
