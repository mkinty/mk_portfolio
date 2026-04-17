import pytest

from apps.techstack.selectors.techstack_selectors import (
    TechStackCategorySelectors,
    TechStackSelectors,
)


@pytest.mark.django_db
class TestTechStackSelectors:
    """
    Test suite for TechStack selectors.
    """

    # -----------------------------
    # TechStackCategorySelectors
    # -----------------------------

    def test_get_category_by_id(self, tech_category):
        """
        Test retrieving category by id.
        """
        category = TechStackCategorySelectors.get_techstack_category_by_id(
            tech_category.id
        )

        assert category == tech_category

    def test_get_all_categories_by_user(self, user, tech_category):
        """
        Test retrieving all categories for a user.
        """
        categories = TechStackCategorySelectors.get_all_tech_stack_categories(user)

        assert categories.count() == 1
        assert categories.first() == tech_category

    # -----------------------------
    # TechStackSelectors
    # -----------------------------

    def test_get_techstack_by_id(self, tech_stack):
        """
        Test retrieving tech stack by id.
        """
        tech = TechStackSelectors.get_tech_stack_by_id(tech_stack.id)

        assert tech == tech_stack

    def test_get_all_by_category(self, tech_category, tech_stack):
        """
        Test retrieving all techs for a category.
        """
        techs = TechStackSelectors.get_all_tech_stack_by_category(tech_category)

        assert techs.count() == 1
        assert techs.first() == tech_stack

    def test_get_all_by_user(self, user, tech_stack):
        """
        Test retrieving all techs for a user.
        """
        techs = TechStackSelectors.get_all_tech_stack_by_user(user)

        assert techs.count() == 1
        assert techs.first() == tech_stack
