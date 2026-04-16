import pytest

from apps.education.models import Education


@pytest.mark.django_db
class TestEducationModels:
    """
    Test suite for Education and EducationSection models.
    """

    def test_education_section_creation(self, education_section, user):
        """
        Test education section creation.
        """
        assert education_section.id is not None
        assert education_section.user == user
        assert education_section.name == "Education"

    def test_education_section_str(self, education_section):
        """
        Test string representation of EducationSection.
        """
        assert str(education_section) == "Education"

    def test_education_creation(self, education_entry, education_section):
        """
        Test education entry creation.
        """
        assert education_entry.id is not None
        assert education_entry.education_section == education_section
        assert education_entry.school == "Test University"
        assert education_entry.degree == "Bachelor of Science"

    def test_education_str(self, education_entry):
        """
        Test string representation of Education.
        """
        assert str(education_entry) == "Bachelor of Science - Test University"

    def test_cascade_delete(self, education_section, education_entry):
        """
        Test cascade delete when section is removed.
        """
        education_id = education_entry.id

        education_section.delete()

        assert Education.objects.filter(id=education_id).exists() is False
