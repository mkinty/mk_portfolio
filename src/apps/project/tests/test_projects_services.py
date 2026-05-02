from datetime import date

import pytest
from apps.project.models import ProjectCategory, Project, Tag
from apps.project.services.projects_services import (
    ProjectCategoryServices,
    ProjectServices, TagServices
)


@pytest.mark.django_db
class TestProjectCategoryServices:
    """Test project category services"""

    def test_get_add_form(self, user):
        """Test getting the add form"""
        form, returned_user = ProjectCategoryServices.get_add_form(user.id)

        assert form is not None
        assert returned_user == user

    def test_create_success(self, user):
        """Test creating a project category successfully"""
        data = {"name": "Backend"}

        success, form, category = ProjectCategoryServices.create(user, data, {})

        assert success is True
        assert form.is_valid()
        assert category is not None
        assert category.name == "Backend"
        assert category.user == user
        assert ProjectCategory.objects.count() == 1

    def test_create_invalid(self, user):
        """Test creating a project category with invalid data"""
        data = {"name": ""}  # invalide

        success, form, category = ProjectCategoryServices.create(user, data, {})

        assert success is False
        assert not form.is_valid()
        assert category is None

    def test_get_update_form(self, category):
        """Test getting the update form"""
        form, returned_category = ProjectCategoryServices.get_update_form(category.id)

        assert form.instance == category
        assert returned_category == category

    def test_update_success(self, category):
        """Test updating a project category successfully"""
        data = {"name": "Updated"}

        success, form, updated_category = ProjectCategoryServices.update(category.id, data, {})

        assert success is True
        assert updated_category.name == "Updated"

    def test_update_invalid(self, category):
        """Test updating a project category with invalid data"""
        data = {"name": ""}

        success, form, updated_category = ProjectCategoryServices.update(category.id, data, {})

        assert success is False
        assert not form.is_valid()

    def test_delete(self, category):
        """Test deleting a project category"""
        result = ProjectCategoryServices.delete(category.id)

        assert result is True
        assert ProjectCategory.objects.count() == 0


@pytest.mark.django_db
class TestTagServices:
    """
    Test tag services
    """

    def test_get_add_form(self):
        """
        Test getting the add form
        """
        form = TagServices.get_add_form()

        assert form is not None

    def test_create_success(self, db):
        """
        Test creating a tag successfully
        """
        data = {"name": "Django"}

        success, form, tag = TagServices.create(data, {})

        assert success is True
        assert form.is_valid()
        assert tag is not None
        assert tag.name == "Django"
        assert Tag.objects.count() == 1

    def test_create_invalid(self, db):
        """
        Test creating a tag with invalid data
        """
        data = {"name": ""}  # invalide

        success, form, tag = TagServices.create(data, {})

        assert success is False
        assert not form.is_valid()
        assert tag is None

    def test_get_update_form(self, tag):
        """
        Test getting the update form
        """
        form, returned_tag = TagServices.get_update_form(tag.id)

        assert form.instance == tag
        assert returned_tag == tag

    def test_update_success(self, tag):
        """
        Test updating a tag successfully
        """
        data = {"name": "Updated Tag"}

        success, form, updated_tag = TagServices.update(tag.id, data, {})

        assert success is True
        assert updated_tag.name == "Updated Tag"

    def test_update_invalid(self, tag):
        """
        Test updating a tag with invalid data
        """
        data = {"name": ""}

        success, form, updated_tag = TagServices.update(tag.id, data, {})

        assert success is False
        assert not form.is_valid()
        assert updated_tag == tag

    def test_delete(self, tag):
        result = TagServices.delete(tag.id)

        assert result is True
        assert Tag.objects.count() == 0

    def test_delete_non_existing_safe(self):
        result = TagServices.delete(999)

        assert result is False


@pytest.mark.django_db
class TestProjectServices:
    """Test project services"""

    def test_create_success(self, user, category):
        """Test creating a project successfully"""
        data = {
            "title": "New Project",
            "category": category.id,
            "start_date": date(2024, 1, 1),
        }

        success, form, project = ProjectServices.create(user, data, {})

        assert success is True
        assert form.is_valid()
        assert project is not None
        assert project.title == "New Project"
        assert project.user == user
        assert Project.objects.count() == 1

    def test_create_invalid(self, user, category):
        """Test creating a project with invalid data"""
        data = {
            "title": "",  # invalide
            "category": category.id,
        }

        success, form, project = ProjectServices.create(user, data, {})

        assert success is False
        assert not form.is_valid()
        assert project is None

    def test_get_update_form(self, project):
        """Test getting the update form"""
        form, returned_project = ProjectServices.get_update_form(project.id)

        assert form.instance == project
        assert returned_project == project

    def test_update_success(self, project, category):
        """Test updating a project successfully"""
        data = {
            "title": "Updated Project",
            "category": category.id,
            "start_date": project.start_date,
        }

        success, form, updated_project = ProjectServices.update(project.id, data, {})

        assert success is True
        assert updated_project.title == "Updated Project"

    def test_update_invalid(self, project, category):
        """Test updating a project with invalid data"""
        data = {
            "title": "",
            "category": category.id,
        }

        success, form, updated_project = ProjectServices.update(project.id, data, {})

        assert success is False
        assert not form.is_valid()

    def test_delete(self, project):
        """Test deleting a project"""
        result = ProjectServices.delete(project.id)

        assert result is True
        assert Project.objects.count() == 0
