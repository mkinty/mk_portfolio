from apps.education.models import Education, EducationSection
from apps.techstack.models import TechStackCategory, TechStack


class TechStackCategorySelectors:
    """
    Selectors for TechStackCategory model
    """

    @staticmethod
    def get_techstack_category_by_id(techstack_category_id):
        """Retrieve a tech stack category by its unique identier"""
        return TechStackCategory.objects.filter(pk=techstack_category_id).first()

    @staticmethod
    def get_all_tech_stack_categories(user):
        """Retrieve all tech stack categories for a user"""
        return (
            user.tech_stack_categories
            .all()
            .prefetch_related("techs")
        )


class TechStackSelectors:
    """
    Selectors for TechStack model
    """

    @staticmethod
    def get_tech_stack_by_id(tech_stack_id):
        """Retrieve a tech stack by its unique identier"""
        return TechStack.objects.filter(pk=tech_stack_id).first()

    @staticmethod
    def get_all_tech_stack_by_category(tech_stack_category):
        """Retrieve all tech stack for a tech stack category"""
        return tech_stack_category.techs.all()

    @staticmethod
    def get_all_tech_stack_by_user(user):
        """Retrieve all tech stack for a user"""
        return user.tech_stacks.all()
