from apps.education.models import Education, EducationSection


class EducationSectionSelectors:
    """
    Selectors for EducationSection model
    """

    @staticmethod
    def get_education_section_by_id(education_section_id):
        """Retrieve an education selection by its unique identier"""
        return EducationSection.objects.filter(pk=education_section_id).first()

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
        return Education.objects.filter(pk=education_id).first()

    @staticmethod
    def get_all_education(education_section):
        """Retrieve all education for an education section"""
        return education_section.educations.all()
