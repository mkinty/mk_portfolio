import pytest

from apps.certifications.models import Certification
from apps.users.models import User


@pytest.fixture
def user(db):
    """
    Create a test user.
    """
    return User.objects.create_user(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="testpass123",
    )


@pytest.fixture
def certification(user):
    """
    Create a test certification.
    """
    return Certification.objects.create(
        user=user, name="AWS Certified Developer", issuer="Amazon", order=1
    )


@pytest.fixture
def certification_factory(user):
    """
    Create a test certification factory.
    """

    def create_cert(**kwargs):
        data = {
            "user": user,
            "name": "Default Cert",
            "issuer": "Default Issuer",
            "order": 0,
        }
        data.update(kwargs)
        return Certification.objects.create(**data)

    return create_cert
