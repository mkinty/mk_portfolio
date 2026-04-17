import pytest

from apps.techstack.models import TechStack


@pytest.mark.django_db
class TestTechStackModels:
    """
    Test suite for TechStackCategory and TechStack models.
    """

    # ----------------------------
    # TechStackCategory tests
    # ----------------------------

    def test_category_creation(self, tech_category, user):
        """
        Test TechStackCategory creation.
        """
        assert tech_category.id is not None
        assert tech_category.user == user
        assert tech_category.name == "Backend"
        assert tech_category.order == 1

    def test_category_str(self, tech_category):
        """
        Test string representation of TechStackCategory.
        """
        assert str(tech_category) == "Backend"

    # ----------------------------
    # TechStack tests
    # ----------------------------

    def test_techstack_creation(self, tech_stack, tech_category, user):
        """
        Test TechStack creation.
        """
        assert tech_stack.id is not None
        assert tech_stack.user == user
        assert tech_stack.category == tech_category
        assert tech_stack.name == "Django"

    def test_techstack_str(self, tech_stack):
        """
        Test string representation of TechStack.
        """
        assert str(tech_stack) == "Django"

    def test_category_reverse_relation(self, tech_stack, tech_category):
        """
        Test reverse relation category -> techs.
        """
        assert tech_category.techs.count() == 1
        assert tech_category.techs.first() == tech_stack

    def test_cascade_delete_category(self, tech_category, tech_stack):
        """
        Test cascade delete when category is removed.
        """
        tech_id = tech_stack.id

        tech_category.delete()

        assert TechStack.objects.filter(id=tech_id).exists() is False
