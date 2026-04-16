import pytest

from apps.education.selectors.education_selectors import (
    EducationSelectors,
    EducationSectionSelectors,
)
from apps.education.models import Education


@pytest.mark.django_db
class TestEducationSelectors:
    """
    Test suite for Education and EducationSection selectors.
    """

    def test_get_education_section(self, education_section):
        """
        Test retrieving a single education section by id.
        """
        section = EducationSectionSelectors.get_education_section(
            education_section.id
        )

        assert section is not None
        assert section == education_section

    def test_get_education_section_not_found(self):
        """
        Test retrieving a non-existing education section.
        """
        section = EducationSectionSelectors.get_education_section(999)

        assert section is None

    def test_get_all_education_sections(self, user, education_section):
        """
        Test retrieving all education sections for a user.
        """
        sections = EducationSectionSelectors.get_all_education_sections(user)

        assert sections.count() == 1
        assert education_section in sections

    def test_get_education(self, education_entry):
        """
        Test retrieving a single education entry by id.
        """
        education = EducationSelectors.get_education(education_entry.id)

        assert education is not None
        assert education == education_entry

    def test_get_education_not_found(self):
        """
        Test retrieving a non-existing education entry.
        """
        education = EducationSelectors.get_education(999)

        assert education is None

    def test_get_all_education(self, education_section, education_entry):
        """
        Test retrieving all education entries for a section.
        """
        educations = EducationSelectors.get_all_education(education_section)

        assert educations.count() == 1
        assert education_entry in educations

    def test_get_all_education_empty(self, education_section):
        """
        Test retrieving educations when none exist.
        """
        educations = EducationSelectors.get_all_education(education_section)

        assert educations.count() == 0
        assert isinstance(educations, type(Education.objects.all()))
