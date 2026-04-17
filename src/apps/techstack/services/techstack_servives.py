from apps.education.selectors.education_selectors import (
    EducationSectionSelectors,
    EducationSelectors
)
from apps.techstack.forms import TechStackCategoryForm, TechStackForm
from apps.techstack.selectors.techstack_selectors import TechStackCategorySelectors, TechStackSelectors
from apps.users.selectors.user_selectors import get_user_by_id


class TechStackCategoryServices:
    """
    Services for managing tech stack categories.
    """

    @staticmethod
    def get_add_form(user_id):
        """
        Get the form for adding a new tech stack category.
        """
        user = get_user_by_id(user_id)

        form = TechStackCategoryForm()
        return form, user

    @staticmethod
    def create(user, data, files):
        """
        Create a new tech stack category.
        """
        form = TechStackCategoryForm(data, files)
        if not form.is_valid():
            return False, form, None

        category = form.save(commit=False)
        category.user = user
        category.save()
        return True, form, category

    @staticmethod
    def get_update_form(category_id):
        """
        Get the form for updating an existing tech stack category.
        """
        category = TechStackCategorySelectors.get_techstack_category_by_id(category_id)
        form = TechStackCategoryForm(instance=category)
        return form, category

    @staticmethod
    def update(category_id, data, files):
        """
        Update an existing tech stack category.
        """
        category = TechStackCategorySelectors.get_techstack_category_by_id(category_id)
        form = TechStackCategoryForm(data, files, instance=category)
        if not form.is_valid():
            return False, form, category
        form.save()
        return True, form, category

    @staticmethod
    def delete(category_id):
        """
        Delete an existing tech stack category.
        """
        category = TechStackCategorySelectors.get_techstack_category_by_id(category_id)
        category.delete()
        return True


class TechStackServices:
    """
    Services for managing tech stacks.
    """

    @staticmethod
    def get_add_form(user_id):
        """
        Get the form for adding a new tech stack.
        """
        user = get_user_by_id(user_id)

        form = TechStackForm()
        return form, user

    @staticmethod
    def create(user, data, files):
        """
        Create a new tech stack.
        """
        form = TechStackForm(data, files)
        if not form.is_valid():
            return False, form, None

        techstack = form.save(commit=False)
        techstack.user = user
        techstack.save()
        return True, form, techstack

    @staticmethod
    def get_update_form(techstack_id):
        """
        Get the form for updating an existing tech stack.
        """
        techstack = TechStackSelectors.get_tech_stack_by_id(techstack_id)
        form = TechStackForm(instance=techstack)
        return form, techstack

    @staticmethod
    def update(techstack_id, data, files):
        """
        Update an existing tech stack.
        """
        techstack = TechStackSelectors.get_tech_stack_by_id(techstack_id)
        form = TechStackForm(data, files, instance=techstack)
        if not form.is_valid():
            return False, form, techstack
        form.save()
        return True, form, techstack

    @staticmethod
    def delete(techstack_id):
        """
        Delete an existing tech stack.
        """
        techstack = TechStackSelectors.get_tech_stack_by_id(techstack_id)
        techstack.delete()
        return True
