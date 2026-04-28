import pytest

from apps.certifications.models import Certification
from apps.certifications.services.certifications_services import CertificationsServices


@pytest.mark.django_db
class TestCertificationsServices:
    """
    Test suite for CertificationsServices
    """

    def test_get_add_certification_form(self, user):
        form, returned_user = CertificationsServices.get_add_certification_form(user.id)

        assert form is not None
        assert returned_user == user

    def test_create_certification_success(self, user):
        data = {
            "name": "AWS Cert",
            "issuer": "Amazon",
            "order": 1
        }

        success, form, certification = CertificationsServices.create_certification(
            user, data, files={}
        )

        assert success is True
        assert form.is_valid()
        assert certification is not None
        assert certification.user == user

    def test_create_certification_invalid(self, user):
        data = {
            "name": "",  # invalide
        }

        success, form, certification = CertificationsServices.create_certification(
            user, data, files={}
        )

        assert success is False
        assert not form.is_valid()
        assert certification is None

    def test_get_update_certification_form(self, certification):

        service = CertificationsServices()
        form, returned_cert = service.get_update_certification_form(certification.id)

        assert form is not None
        assert returned_cert == certification

    def test_update_certification_success(self, certification):

        data = {
            "name": "Updated Cert",
            "issuer": "Updated Org",
            "order": 2
        }

        success, form, updated_cert = CertificationsServices.update_certification(
            certification.id, data, files={}
        )

        assert success is True
        assert form.is_valid()
        assert updated_cert.name == "Updated Cert"

    def test_update_certification_invalid(self, certification):

        data = {
            "name": "",  # invalide
        }

        success, form, updated_cert = CertificationsServices.update_certification(
            certification.id, data, files={}
        )

        assert success is False
        assert not form.is_valid()
        assert updated_cert == certification

    def test_delete_certification(self, certification):

        result = CertificationsServices.delete_certification(certification.id)

        assert result is True
        assert Certification.objects.filter(id=certification.id).exists() is False
