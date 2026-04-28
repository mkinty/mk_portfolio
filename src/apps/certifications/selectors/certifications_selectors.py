from apps.certifications.models import Certification


class CertificationsSelectors:
    """
    Selectors for certification-related queries.
    """

    @staticmethod
    def get_certifications_for_user(user):
        """
        Get all certifications for a user.
        """
        return Certification.objects.filter(user=user)

    @staticmethod
    def get_certification_by_id(certification_id):
        """
        Get a certification by ID.
        """
        try:
            return Certification.objects.get(id=certification_id)
        except Certification.DoesNotExist:
            return None
