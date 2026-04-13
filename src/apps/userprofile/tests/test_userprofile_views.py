import pytest
from django.urls import reverse
from apps.userprofile.models import UserProfile


def test_userprofile_index_view(client, user):
    """
    Test that the userprofile index view returns the user object in the context
    """
    url = reverse("userprofile:index", kwargs={"user_id": user.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "user_obj" in response.context
    assert response.context["user_obj"] == user


@pytest.mark.django_db
def test_userprofile_view(client, user):
    """
    Test that the userprofile detail view returns the user object in the context
    """
    url = reverse("userprofile:detail", kwargs={"user_id": user.id})

    response = client.get(url)

    assert response.status_code == 200
    assert "userprofile" in response.context


@pytest.mark.django_db
def test_userprofile_view_not_found(client, user):
    """
    Test that the userprofile view returns a 404 if the user has no profile
    """
    user.profile.delete()

    url = reverse("userprofile:detail", kwargs={"user_id": user.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "Profil utilisateur" in response.content.decode()


@pytest.mark.django_db
def test_add_userprofile_get(client, user):
    """
    Test that the add userprofile get view returns the form in the context
    """
    user.profile.delete()

    url = reverse("userprofile:add-profile", kwargs={"user_id": user.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["user_obj"] == user


@pytest.mark.django_db
def test_add_userprofile_post_success(client, user):
    """
    Test that the add userprofile post view creates a new profile
    """
    user.profile.delete()

    url = reverse("userprofile:add-profile", kwargs={"user_id": user.id})

    data = {"bio": "Test bio"}

    response = client.post(url, data)

    assert response.status_code == 200
    assert response.headers["HX-Trigger"] == "formSubmittedEvent"
    assert UserProfile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_update_userprofile_get(client, user_profile):
    """
    Test that the update userprofile get view returns the form in the context
    """
    url = reverse("userprofile:update-profile", kwargs={"userprofile_id": user_profile.id})

    response = client.get(url)

    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["userprofile"] == user_profile


@pytest.mark.django_db
def test_update_userprofile_post(client, user_profile):
    """
    Test that the update userprofile post view updates the profile
    """
    url = reverse("userprofile:update-profile", kwargs={"userprofile_id": user_profile.id})

    data = {"bio": "Updated bio"}

    response = client.post(url, data)

    assert response.status_code == 200
    assert response.headers["HX-Trigger"] == "formSubmittedEvent"


@pytest.mark.django_db
def test_delete_userprofile_get(client, user_profile):
    """
    Test that the delete userprofile get view returns the confirmation page
    """
    url = reverse("userprofile:delete-profile", kwargs={"userprofile_id": user_profile.id})

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_userprofile_post(client, user_profile):
    """
    Test that the delete userprofile post view deletes the profile
    """
    url = reverse("userprofile:delete-profile", kwargs={"userprofile_id": user_profile.id})

    response = client.post(url)

    assert response.status_code == 200
    assert response.headers["HX-Trigger"] == "formSubmittedEvent"

    assert not UserProfile.objects.filter(id=user_profile.id).exists()