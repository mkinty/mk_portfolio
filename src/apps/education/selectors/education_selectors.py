from apps.education.models import Education, EducationSection


class EducationSectionSelectors:
    """
    Selectors for EducationSection model
    """

    @staticmethod
    def get_education_section_by_id(education_section_id):
        """Retrieve an education selection by its unique identier"""
        try:
            return EducationSection.objects.get(pk=education_section_id)
        except EducationSection.DoesNotExist:
            return None

    @staticmethod
    def get_all_education_sections(user):
        """Retrieve all education sections for a user"""
        return (
            user.education_sections
            .all()
            .prefetch_related("educations")
        )


class EducationSelectors:
    """
    Selectors for Education model
    """

    @staticmethod
    def get_education_by_id(education_id):
        """Retrieve an education by its unique identier"""
        try:
            return Education.objects.get(pk=education_id)
        except Education.DoesNotExist:
            return None

    @staticmethod
    def get_all_education(education_section):
        """Retrieve all education for an education section"""
        return education_section.educations.all()
