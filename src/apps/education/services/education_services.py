from apps.education.forms import EducationForm, EducationSectionForm
from apps.education.selectors.education_selectors import EducationSectionSelectors, EducationSelectors
from apps.users.selectors.user_selectors import get_user_by_id


class EducationSectionServices:
    """
    Services for managing education sections.
    """
    @staticmethod
    def get_add_form(user_id):
        """
        Get the form for adding a new education section.
        """
        user = get_user_by_id(user_id)

        form = EducationSectionForm()
        return form, user

    @staticmethod
    def create(user, data, files):
        """
        Create a new education section.
        """
        form = EducationSectionForm(data, files)
        if not form.is_valid():
            return False, form, None

        education_section = form.save(commit=False)
        education_section.user = user
        education_section.save()
        return True, form, education_section

    @staticmethod
    def get_update_form(education_section_id):
        """
        Get the form for updating an existing education section.
        """
        education_section = EducationSectionSelectors.get_education_section_by_id(education_section_id)
        form = EducationSectionForm(instance=education_section)
        return form, education_section

    @staticmethod
    def update(education_section_id, data, files):
        """
        Update an existing education section.
        """
        education_section = EducationSectionSelectors.get_education_section_by_id(education_section_id)
        form = EducationSectionForm(data, files, instance=education_section)
        if not form.is_valid():
            return False, form, education_section
        form.save()
        return True, form, education_section

    @staticmethod
    def delete(education_section_id):
        """
        Delete an existing education section.
        """
        education_section = EducationSectionSelectors.get_education_section_by_id(education_section_id)
        education_section.delete()
        return True


class EducationServices:
    """
    Services for managing education items.
    """

    @staticmethod
    def get_add_form(education_section_id):
        """
        Get the form for adding a new education item.
        """
        education_section = EducationSectionSelectors.get_education_section_by_id(education_section_id)

        form = EducationForm()
        return form, education_section

    @staticmethod
    def create(education_section, data, files):
        """
        Create a new education item.
        """
        form = EducationForm(data, files)
        if not form.is_valid():
            return False, form, None

        education = form.save(commit=False)
        education.education_section = education_section
        education.save()
        return True, form, education

    @staticmethod
    def get_update_form(education_id):
        """
        Get the form for updating an existing education item.
        """
        education = EducationSelectors.get_education_by_id(education_id)
        form = EducationForm(instance=education)
        return form, education

    @staticmethod
    def update(education_id, data, files):
        """
        Update an existing education item.
        """
        education = EducationSelectors.get_education_by_id(education_id)
        form = EducationForm(data, files, instance=education)
        if not form.is_valid():
            return False, form, education
        form.save()
        return True, form, education

    @staticmethod
    def delete(education_id):
        """
        Delete an existing education item.
        """
        education = EducationSelectors.get_education_by_id(education_id)
        education.delete()
        return True