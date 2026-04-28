import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestCertificationsAddView:
    """
    Test cases for the CertificationsAddView.
    """

    def test_add_view_get(self, client, user):
        """
        Test that the add view returns a 200 status code and includes a form in the context.
        """
        url = reverse("certifications:add", args=[user.id])
        response = client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_add_view_post_success(self, client, user):
        """
        Test that the add view returns a 200 status code when a valid certification is created.
        """
        url = reverse("certifications:add", args=[user.id])
        response = client.post(url, data={"name": "Cert"})

        assert response.status_code == 200

    def test_add_view_post_error(self, client, user):
        """
        Test that the add view returns a 200 status code when an invalid certification is created.
        """
        url = reverse("certifications:add", args=[user.id])
        response = client.post(url, data={})

        assert response.status_code == 200
        assert "form" in response.context


@pytest.mark.django_db
class TestCertificationsUpdateView:
    """
    Test cases for the CertificationsUpdateView.
    """

    def test_update_view_get(self, client, certification):
        """
        Test that the update view returns a 200 status code.
        """
        url = reverse("certifications:update", args=[certification.id])
        response = client.get(url)

        assert response.status_code == 200

    def test_update_view_post_success(self, client, certification):
        """
        Test that the update view returns a 200 status code when a valid certification is updated.
        """
        url = reverse("certifications:update", args=[certification.id])
        response = client.post(url, data={"name": "Updated"})

        assert response.status_code == 200

    def test_update_view_post_error(self, client, certification):
        """
        Test that the update view returns a 200 status code when an invalid certification is updated.
        """
        url = reverse("certifications:update", args=[certification.id])
        response = client.post(url, data={})

        assert response.status_code == 200
        assert "form" in response.context


@pytest.mark.django_db
class TestCertificationsDeleteView:
    """
    Test cases for the CertificationsDeleteView.
    """

    def test_delete_view_get(self, client, certification):
        """
        Test that the delete view returns a 200 status code.
        """
        url = reverse("certifications:delete", args=[certification.id])
        response = client.get(url)

        assert response.status_code == 200

    def test_delete_view_post_success(self, client, certification):
        """
        Test that the delete view returns a 200 status code when a valid certification is deleted.
        """
        url = reverse("certifications:delete", args=[certification.id])
        response = client.post(url)

        assert response.status_code == 200
