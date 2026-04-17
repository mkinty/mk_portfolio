import pytest

from apps.techstack.models import TechStackCategory, TechStack
from apps.techstack.services.techstack_servives import TechStackCategoryServices, TechStackServices


@pytest.mark.django_db
class TestTechStackCategoryServices:
    """
    Test suite for TechStackCategoryServices.
    """

    def test_get_add_form(self, user):
        form, returned_user = TechStackCategoryServices.get_add_form(user.id)

        assert form is not None
        assert returned_user == user

    def test_create_category_success(self, user):
        data = {
            "name": "Backend",
            "order": 1,
        }

        success, form, category = TechStackCategoryServices.create(user, data, {})

        assert success is True
        assert category is not None
        assert category.name == "Backend"
        assert category.user == user
        assert TechStackCategory.objects.count() == 1

    def test_create_category_invalid(self, user):
        data = {
            "name": "",  # invalide
        }

        success, form, category = TechStackCategoryServices.create(user, data, {})

        assert success is False
        assert category is None
        assert form.errors

    def test_get_update_form(self, tech_category):
        form, category = TechStackCategoryServices.get_update_form(
            tech_category.id
        )

        assert form.instance == tech_category
        assert category == tech_category

    def test_update_category_success(self, tech_category):
        data = {
            "name": "Frontend",
            "order": 2,
        }

        success, form, category = TechStackCategoryServices.update(
            tech_category.id,
            data,
            {}
        )

        category.refresh_from_db()

        assert success is True
        assert category.name == "Frontend"

    def test_delete_category(self, tech_category):
        success = TechStackCategoryServices.delete(tech_category.id)

        assert success is True
        assert TechStackCategory.objects.count() == 0


@pytest.mark.django_db
class TestTechStackServices:
    """
    Test suite for TechStackServices.
    """

    def test_get_add_form(self, user):
        form, user = TechStackServices.get_add_form(user.id)

        assert form is not None
        assert user == user

    def test_create_techstack_success(self, user):
        category = TechStackCategory.objects.create(
            name="Backend",
            user=user,
            order=1,
        )

        data = {
            "name": "Django",
            "category": category,
        }

        success, form, techstack = TechStackServices.create(
            user,
            data,
            {}
        )

        assert success is True
        assert techstack is not None
        assert techstack.name == "Django"
        assert techstack.category == category
        assert techstack.user == user
        assert TechStack.objects.count() == 1

    def test_create_techstack_invalid(self, tech_category):
        data = {
            "name": "",  # invalide
        }

        success, form, techstack = TechStackServices.create(
            tech_category,
            data,
            {}
        )

        assert success is False
        assert techstack is None
        assert form.errors

    def test_get_update_form(self, tech_stack):
        form, techstack = TechStackServices.get_update_form(tech_stack.id)

        assert form.instance == tech_stack
        assert techstack == tech_stack

    def test_update_techstack_success(self, tech_stack):
        data = {
            "name": "FastAPI",
            "category": tech_stack.category.id,
        }

        success, form, techstack = TechStackServices.update(
            tech_stack.id,
            data,
            {}
        )

        techstack.refresh_from_db()

        assert success is True
        assert techstack.name == "FastAPI"

    def test_delete_techstack(self, tech_stack):
        success = TechStackServices.delete(tech_stack.id)

        assert success is True
        assert TechStack.objects.count() == 0
