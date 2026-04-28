import pytest

from apps.certifications.models import Certification


@pytest.mark.django_db
def test_certification_creation(user, certification):
    """
    Test that a certification can be created with the correct fields.
    """
    assert certification.name == "AWS Certified Developer"
    assert certification.issuer == "Amazon"
    assert certification.order == 1
    assert certification.user is not None


@pytest.mark.django_db
def test_certification_str(certification):
    """
    Test that the string representation of a certification is correct.
    """
    assert str(certification) == "AWS Certified Developer"


@pytest.mark.django_db
def test_user_certifications_related_name(user, certification):
    """
    Test that the related name for certifications works correctly.
    """
    certifications = user.certifications.all()
    assert certifications.count() == 1
    assert certifications.first() == certification


@pytest.mark.django_db
def test_certification_ordering(certification_factory):
    """
    Test that certifications are ordered by their order field.
    """
    certa = certification_factory(name="Cert B", order=2)
    certb = certification_factory(name="Cert A", order=1)

    certifications = Certification.objects.all()

    assert certifications[0].name == "Cert A"
    assert certifications[1].name == "Cert B"
    assert certa != certb
