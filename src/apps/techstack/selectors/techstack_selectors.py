from apps.techstack.models import TechStack, TechStackCategory


class TechStackCategorySelectors:
    """
    Selectors for TechStackCategory model
    """

    @staticmethod
    def get_techstack_category_by_id(techstack_category_id):
        """Retrieve a tech stack category by its unique identier"""
        try:
            return TechStackCategory.objects.get(pk=techstack_category_id)
        except TechStackCategory.DoesNotExist:
            return None

    @staticmethod
    def get_all_tech_stack_categories(user):
        """Retrieve all tech stack categories for a user"""
        return user.tech_stack_categories.all().prefetch_related("techs")


class TechStackSelectors:
    """
    Selectors for TechStack model
    """

    @staticmethod
    def get_tech_stack_by_id(tech_stack_id):
        """Retrieve a tech stack by its unique identier"""
        try:
            return TechStack.objects.get(pk=tech_stack_id)
        except TechStack.DoesNotExist:
            return None

    @staticmethod
    def get_all_tech_stack_by_category(tech_stack_category):
        """Retrieve all tech stack for a tech stack category"""
        return tech_stack_category.techs.all()

    @staticmethod
    def get_all_tech_stack_by_user(user):
        """Retrieve all tech stack for a user"""
        return user.tech_stacks.all()
