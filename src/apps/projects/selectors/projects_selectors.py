from apps.projects.models import ProjectCategory, Project


class ProjectCategorySelectors:
    """
    Selectors for ProjectCategory model
    """
    @staticmethod
    def get_project_category_by_id(project_category_id):
        """
        Get a project category by its ID
        """
        try:
            return ProjectCategory.objects.get(pk=project_category_id)
        except ProjectCategory.DoesNotExist:
            return None

    @staticmethod
    def get_project_categories():
        """
        Get all project categories
        """
        return ProjectCategory.objects.all()


class ProjectSelectors:
    """Selectors for Project model"""
    @staticmethod
    def get_project_by_id(project_id):
        """
        Get a project by its ID
        """
        try:
            return Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return None

    @staticmethod
    def get_projects():
        """
        Get all projects
        """
        return Project.objects.all()

    @staticmethod
    def get_projects_by_category(category):
        """
        Get projects by category
        """
        return category.projects.all()

    @staticmethod
    def get_projects_by_user(user):
        """
        Get projects by user
        """
        return user.user_projects.all()
