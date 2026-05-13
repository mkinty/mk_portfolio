from apps.project.forms import ProjectCategoryForm, ProjectForm, TagForm
from apps.project.selectors.projects_selectors import (
    ProjectCategorySelectors,
    ProjectSelectors,
    TagSelectors,
)
from apps.users.selectors.user_selectors import get_user_by_id


class ProjectCategoryServices:
    """
    Service class for project category operations.
    """

    @staticmethod
    def get_add_form(user_id):
        """
        Get the form for adding a new project category.
        """
        user = get_user_by_id(user_id)
        form = ProjectCategoryForm()
        return form, user

    @staticmethod
    def create(user, data, files):
        """
        Create a new project category.
        """
        form = ProjectCategoryForm(data, files)
        if not form.is_valid():
            return False, form, None
        category = form.save(commit=False)
        category.user = user
        category.save()
        return True, form, category

    @staticmethod
    def get_update_form(category_id):
        """
        Get the form for updating an existing project category.
        """
        category = ProjectCategorySelectors.get_project_category_by_id(category_id)
        form = ProjectCategoryForm(instance=category)
        return form, category

    @staticmethod
    def update(category_id, data, files):
        """
        Update an existing project category.
        """
        category = ProjectCategorySelectors.get_project_category_by_id(category_id)
        form = ProjectCategoryForm(data, files, instance=category)
        if not form.is_valid():
            return False, form, category
        form.save()
        return True, form, category

    @staticmethod
    def delete(category_id):
        """
        Delete an existing project category.
        """
        category = ProjectCategorySelectors.get_project_category_by_id(category_id)
        if not category:
            return False
        category.delete()
        return True


class TagServices:
    """
    Service class for tag operations.
    """

    @staticmethod
    def get_add_form():
        """
        Get the form for adding a new tag.
        """
        form = TagForm()
        return form

    @staticmethod
    def create(data, files):
        """
        Create a new tag.
        """
        form = TagForm(data, files)
        if not form.is_valid():
            return False, form, None
        tag = form.save()
        return True, form, tag

    @staticmethod
    def get_update_form(tag_id):
        """
        Get the form for updating an existing tag.
        """
        tag = TagSelectors.get_tag_by_id(tag_id)
        form = TagForm(instance=tag)
        return form, tag

    @staticmethod
    def update(tag_id, data, files):
        """
        Update an existing tag.
        """
        tag = TagSelectors.get_tag_by_id(tag_id)
        form = TagForm(data, files, instance=tag)
        if not form.is_valid():
            return False, form, tag
        form.save()
        return True, form, tag

    @staticmethod
    def delete(tag_id):
        """
        Delete an existing tag.
        """
        tag = TagSelectors.get_tag_by_id(tag_id)
        if not tag:
            return False
        tag.delete()
        return True


class ProjectServices:
    """
    Service class for project operations.
    """

    @staticmethod
    def get_add_form(user_id):
        """
        Get the form for adding a new project.
        """
        user = get_user_by_id(user_id)
        form = ProjectForm()
        return form, user

    @staticmethod
    def create(user, data, files):
        """
        Create a new project.
        """
        form = ProjectForm(data, files)
        if not form.is_valid():
            return False, form, None
        project = form.save(commit=False)
        project.user = user
        project.save()
        form.save_m2m()  # Save many-to-many relationships
        return True, form, project

    @staticmethod
    def get_update_form(project_id):
        """
        Get the form for updating an existing project.
        """
        project = ProjectSelectors.get_project_by_id(project_id)
        form = ProjectForm(instance=project)
        return form, project

    @staticmethod
    def update(project_id, data, files):
        """
        Update an existing project.
        """
        project = ProjectSelectors.get_project_by_id(project_id)
        form = ProjectForm(data, files, instance=project)
        if not form.is_valid():
            return False, form, project
        form.save()
        return True, form, project

    @staticmethod
    def delete(project_id):
        """
        Delete an existing project.
        """
        project = ProjectSelectors.get_project_by_id(project_id)
        if not project:
            return False
        project.delete()
        return True
