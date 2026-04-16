import pytest

from apps.education.models import Education, EducationSection
from apps.education.services.education_services import (
    EducationSectionServices,
    EducationServices,
)


@pytest.mark.django_db
class TestEducationServices:
    """
    Test suite for EducationSectionServices and EducationServices.
    """

    # ----------------------------------------------------------------
    # Education Section Services
    # ----------------------------------------------------------------

    def test_get_add_section_form(self, user):
        """
        Test retrieving add form for education section.
        """
        form, returned_user = EducationSectionServices.get_add_form(user.id)

        assert form is not None
        assert returned_user == user

    def test_create_section_success(self, user):
        """
        Test creating education section successfully.
        """
        data = {
            "name": "Academic Background",
            "description": "My academic journey",
        }

        success, form, section = EducationSectionServices.create(
            user=user,
            data=data,
            files=None,
        )

        assert success is True
        assert section is not None
        assert isinstance(section, EducationSection)
        assert section.user == user
        assert section.name == "Academic Background"

    def test_create_section_failure(self, user):
        """
        Test creating education section failure.
        """
        data = {
            "name": "",
        }

        success, form, section = EducationSectionServices.create(
            user=user,
            data=data,
            files=None,
        )

        assert success is False
        assert section is None
        assert form.errors

    def test_get_update_section_form(self, education_section):
        """
        Test retrieving update form for section.
        """
        form, section = EducationSectionServices.get_update_form(
            education_section.id
        )

        assert form is not None
        assert section == education_section
        assert form.instance == education_section

    def test_update_section_success(self, education_section):
        """
        Test updating education section successfully.
        """
        data = {
            "name": "Updated Section",
            "description": "Updated description",
        }

        success, form, updated_section = EducationSectionServices.update(
            education_section_id=education_section.id,
            data=data,
            files=None,
        )

        updated_section.refresh_from_db()

        assert success is True
        assert updated_section.name == "Updated Section"

    def test_delete_section(self, education_section):
        """
        Test deleting education section.
        """
        section_id = education_section.id

        success = EducationSectionServices.delete(section_id)

        assert success is True
        assert EducationSection.objects.filter(id=section_id).exists() is False

    # ----------------------------------------------------------------
    # Education Services
    # ----------------------------------------------------------------

    def test_get_add_education_form(self, education_section):
        """
        Test retrieving add form for education.
        """
        form, returned_education_section = EducationServices.get_add_form(education_section.id)

        assert form is not None
        assert returned_education_section == education_section

    def test_create_education_success(self, education_section):
        """
        Test creating education successfully.
        """
        data = {
            "school": "MIT",
            "degree": "Master",
            "field_of_study": "Computer Science",
            "start_date": "2020-01-01",
            "end_date": "2022-01-01",
            "description": "Test description",
        }

        success, form, education = EducationServices.create(
            education_section=education_section,
            data=data,
            files=None,
        )

        assert success is True
        assert education is not None
        assert isinstance(education, Education)

    def test_create_education_failure(self, education_section):
        """
        Test creating education failure.
        """
        data = {}

        success, form, education = EducationServices.create(
            education_section=education_section,
            data=data,
            files=None,
        )

        assert success is False
        assert education is None
        assert form.errors

    def test_get_update_education_form(self, education_entry):
        """
        Test retrieving update form for education.
        """
        form, education = EducationServices.get_update_form(
            education_entry.id
        )

        assert form is not None
        assert education == education_entry
        assert form.instance == education_entry

    def test_update_education_success(self, education_entry):
        """
        Test updating education successfully.
        """
        data = {
            "education_section": education_entry.education_section.id,
            "school": "Updated University",
            "degree": "Updated Degree",
            "field_of_study": "AI",
            "start_date": "2020-01-01",
            "end_date": "2023-01-01",
            "description": "Updated",
        }

        success, form, updated = EducationServices.update(
            education_id=education_entry.id,
            data=data,
            files=None,
        )

        updated.refresh_from_db()

        assert success is True
        assert updated.school == "Updated University"

    def test_delete_education(self, education_entry):
        """
        Test deleting education.
        """
        education_id = education_entry.id

        success = EducationServices.delete(education_id)

        assert success is True
        assert Education.objects.filter(id=education_id).exists() is False
