from apps.project.models import Project, ProjectCategory, Tag


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


class TagSelectors:
    """
    Selectors for Tag model
    """

    @staticmethod
    def get_tag_by_id(tag_id):
        """
        Get a tag by its ID
        """
        try:
            return Tag.objects.get(pk=tag_id)
        except Tag.DoesNotExist:
            return None

    @staticmethod
    def get_tags():
        """
        Get all tags
        """
        return Tag.objects.all()


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

    @staticmethod
    def get_projects_by_tag(tag):
        """
        Get projects by tag (case-insensitive)
        """
        return Project.objects.filter(tags__name__iexact=str(tag).strip()).distinct()
