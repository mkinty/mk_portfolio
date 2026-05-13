import pytest
from django.urls import reverse

from apps.userprofile.models import UserProfile


@pytest.mark.django_db
class TestUserProfileViews:
    """
    Test suite for UserProfile views.
    """

    def test_userprofile_index_view(self, client, user):
        """
        Test index view returns user in context.
        """
        url = reverse("userprofile:index", kwargs={"user_id": user.id})
        response = client.get(url)

        assert response.status_code == 200
        assert "user_obj" in response.context
        assert response.context["user_obj"] == user

    def test_userprofile_detail_view(self, client, user, user_profile):
        """
        Test detail view returns userprofile in context.
        """
        url = reverse("userprofile:detail", kwargs={"user_id": user.id})
        response = client.get(url)

        assert response.status_code == 200
        assert "userprofile" in response.context

    def test_userprofile_detail_view_no_profile(self, client, user):
        """
        Test detail view when profile does not exist.
        """
        user.profile.delete()

        url = reverse("userprofile:detail", kwargs={"user_id": user.id})
        response = client.get(url)

        assert response.status_code == 200
        assert "Profil utilisateur" in response.content.decode()

    def test_add_userprofile_get(self, client, user):
        """
        Test GET add profile view returns form.
        """
        user.profile.delete()

        url = reverse("userprofile:add", kwargs={"user_id": user.id})
        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["user_obj"] == user

    def test_add_userprofile_post_success(self, client, user):
        """
        Test POST add profile creates new profile.
        """
        user.profile.delete()

        url = reverse("userprofile:add", kwargs={"user_id": user.id})
        data = {"bio": "Test bio"}

        response = client.post(url, data)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"
        assert UserProfile.objects.filter(user=user).exists()

    def test_update_userprofile_get(self, client, user_profile):
        """
        Test GET update profile view returns form.
        """
        url = reverse("userprofile:update", kwargs={"userprofile_id": user_profile.id})

        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context
        assert response.context["userprofile"] == user_profile

    def test_update_userprofile_post(self, client, user_profile):
        """
        Test POST update profile updates data.
        """
        url = reverse("userprofile:update", kwargs={"userprofile_id": user_profile.id})

        data = {"bio": "Updated bio"}

        response = client.post(url, data)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    def test_delete_userprofile_get(self, client, user_profile):
        """
        Test GET delete confirmation view.
        """
        url = reverse("userprofile:delete", kwargs={"userprofile_id": user_profile.id})

        response = client.get(url)

        assert response.status_code == 200

    def test_delete_userprofile_post(self, client, user_profile):
        """
        Test POST delete removes profile.
        """
        url = reverse("userprofile:delete", kwargs={"userprofile_id": user_profile.id})

        response = client.post(url)

        assert response.status_code == 200
        assert response.headers["HX-Trigger"] == "formSubmittedEvent"
        assert not UserProfile.objects.filter(id=user_profile.id).exists()
