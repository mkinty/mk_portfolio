from apps.certifications.forms import CertificationForm
from apps.certifications.selectors.certifications_selectors import (
    CertificationsSelectors,
)
from apps.users.selectors.user_selectors import get_user_by_id


class CertificationsServices:
    """
    Services for certification-related operations.
    """

    @staticmethod
    def get_add_certification_form(user_id):
        """
        Get the form for adding a new certification.
        """
        user = get_user_by_id(user_id)
        form = CertificationForm()
        return form, user

    @staticmethod
    def create_certification(user, data, files):
        """
        Create a new certification.
        """
        form = CertificationForm(data, files)
        if not form.is_valid():
            return False, form, None

        certification = form.save(commit=False)
        certification.user = user
        certification.save()
        return True, form, certification

    @staticmethod
    def get_update_certification_form(certification_id):
        """
        Get the form for editing an existing certification.
        """
        certification = CertificationsSelectors.get_certification_by_id(
            certification_id
        )
        form = CertificationForm(instance=certification)
        return form, certification

    @staticmethod
    def update_certification(certification_id, data, files):
        """
        Update an existing certification.
        """
        certification = CertificationsSelectors.get_certification_by_id(
            certification_id
        )
        form = CertificationForm(data, files, instance=certification)
        if not form.is_valid():
            return False, form, certification

        form.save()
        return True, form, certification

    @staticmethod
    def delete_certification(certification_id):
        """
        Delete a certification.
        """
        certification = CertificationsSelectors.get_certification_by_id(
            certification_id
        )
        if not certification:
            return False
        certification.delete()
        return True
