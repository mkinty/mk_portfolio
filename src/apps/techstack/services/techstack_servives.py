from apps.techstack.forms import TechStackCategoryForm, TechStackForm
from apps.techstack.selectors.techstack_selectors import (
    TechStackCategorySelectors,
    TechStackSelectors,
)
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
        if not category:
            return False
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

        tech_stack = form.save(commit=False)
        tech_stack.user = user
        tech_stack.save()
        return True, form, tech_stack

    @staticmethod
    def get_update_form(tech_stack_id):
        """
        Get the form for updating an existing tech stack.
        """
        tech_stack = TechStackSelectors.get_tech_stack_by_id(tech_stack_id)
        form = TechStackForm(instance=tech_stack)
        return form, tech_stack

    @staticmethod
    def update(tech_stack_id, data, files):
        """
        Update an existing tech stack.
        """
        tech_stack = TechStackSelectors.get_tech_stack_by_id(tech_stack_id)
        form = TechStackForm(data, files, instance=tech_stack)
        if not form.is_valid():
            return False, form, tech_stack
        form.save()
        return True, form, tech_stack

    @staticmethod
    def delete(tech_stack_id):
        """
        Delete an existing tech stack.
        """
        tech_stack = TechStackSelectors.get_tech_stack_by_id(tech_stack_id)
        if not tech_stack:
            return False
        tech_stack.delete()
        return True
