import pytest

from apps.certifications.selectors.certifications_selectors import CertificationsSelectors

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_get_certifications_for_user_returns_user_certifications(user, certification):
    """
    Test that get_certifications_for_user returns only the certifications for the given user.
    """
    result = CertificationsSelectors.get_certifications_for_user(user)

    assert result.count() == 1
    assert result.first() == certification


@pytest.mark.django_db
def test_get_certifications_for_user_returns_empty_queryset():
    """
    Test that get_certifications_for_user return empty queryset
    """
    result = CertificationsSelectors.get_certifications_for_user(None)

    assert result.count() == 0


@pytest.mark.django_db
def test_get_certification_by_id_returns_correct_object(certification):
    """
    Test that get_certification_by_id return a certification by id
    """
    result = CertificationsSelectors.get_certification_by_id(certification.id)

    assert result == certification


@pytest.mark.django_db
def test_get_certification_by_id_returns_none_if_not_found():
    """
    Test that get_certification_by_id return none
    """
    result = CertificationsSelectors.get_certification_by_id(9999)

    assert result is None
