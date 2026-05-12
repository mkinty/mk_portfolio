import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from apps.tracking.services.applications_services import (
    ApplicationsServices,
    FollowUpServices,
)
from apps.tracking.models import ApplicationStatus, FollowUpStatus


# =========================================================
# ApplicationsServices
# =========================================================

@pytest.mark.django_db
class TestApplicationsServices:

    def test_get_add_form(self, user):
        form, returned_user = ApplicationsServices.get_add_form(user.id)

        assert form is not None
        assert returned_user == user

    def test_create_valid(self, user):
        data = {
            "position": "Backend Developer",
            "company": "OpenAI",
            "job_offer_link": "https://openai.com",
            "application_date": "2024-01-01",
            "application_status": ApplicationStatus.SENT,
        }

        files = {
            "resume": SimpleUploadedFile(
                "cv.pdf",
                b"fake-cv-content"
            )
        }

        success, form, application = ApplicationsServices.create(
            user=user,
            data=data,
            files=files,
        )

        assert success is True
        assert application is not None
        assert application.user == user
        assert application.position == "Backend Developer"

    def test_create_invalid(self, user):
        data = {}  # invalid form

        success, form, application = ApplicationsServices.create(
            user=user,
            data=data,
            files={}
        )

        assert success is False
        assert application is None
        assert form.errors

    def test_get_update_form(self, job_application):
        form, application = ApplicationsServices.get_update_form(
            job_application.id
        )

        assert form is not None
        assert application == job_application

    def test_get_update_form_not_found(self):
        form, application = ApplicationsServices.get_update_form(999999)

        assert form is None
        assert application is None

    def test_update_valid(self, job_application):
        data = {
            "position": "Updated Position",
            "company": job_application.company,
            "application_date": "2024-01-01",
            "application_status": ApplicationStatus.SENT,
        }

        success, form, application = ApplicationsServices.update(
            job_application.id,
            data,
            files={}
        )

        assert success is True
        assert application.position == "Updated Position"

    def test_update_invalid(self, job_application):
        data = {}  # invalid

        success, form, application = ApplicationsServices.update(
            job_application.id,
            data,
            files={}
        )

        assert success is False
        assert application is None
        assert form.errors

    def test_delete(self, job_application):
        success = ApplicationsServices.delete(job_application.id)

        assert success is True

    def test_delete_not_found(self):
        success = ApplicationsServices.delete(999999)

        assert success is False


# =========================================================
# FollowUpServices
# =========================================================

@pytest.mark.django_db
class TestFollowUpServices:

    def test_get_add_form(self, job_application):
        form, application = FollowUpServices.get_add_form(
            job_application.id
        )

        assert form is not None
        assert application == job_application

    def test_get_add_form_not_found(self):
        form, application = FollowUpServices.get_add_form(999999)

        assert form is None
        assert application is None

    def test_create_valid(self, job_application):
        data = {
            "title": "Premier entretien RH",
            "event_date": "2024-01-01",
            "status": FollowUpStatus.PENDING,
        }

        success, form, follow_up = FollowUpServices.create(
            application=job_application,
            data=data,
            files={}
        )

        assert success is True
        assert follow_up is not None
        assert follow_up.job_application == job_application
        assert follow_up.title == "Premier entretien RH"

    def test_create_invalid(self, job_application):
        data = {}

        success, form, follow_up = FollowUpServices.create(
            application=job_application,
            data=data,
            files={}
        )

        assert success is False
        assert follow_up is None
        assert form.errors

    def test_get_update_form(self, follow_up):
        form, instance = FollowUpServices.get_update_form(
            follow_up.id
        )

        assert form is not None
        assert instance == follow_up

    def test_get_update_form_not_found(self):
        form, instance = FollowUpServices.get_update_form(999999)

        assert form is None
        assert instance is None

    def test_update_valid(self, follow_up):
        data = {
            "title": "Updated Follow Up",
            "event_date": "2024-01-01",
            "status": FollowUpStatus.PENDING,
        }

        success, form, instance = FollowUpServices.update(
            follow_up.id,
            data,
            files={}
        )

        assert success is True
        assert instance.title == "Updated Follow Up"

    def test_update_invalid(self, follow_up):
        data = {}

        success, form, instance = FollowUpServices.update(
            follow_up.id,
            data,
            files={}
        )

        assert success is False
        assert instance is None
        assert form.errors

    def test_delete(self, follow_up):
        success = FollowUpServices.delete(follow_up.id)

        assert success is True

    def test_delete_not_found(self):
        success = FollowUpServices.delete(999999)

        assert success is False
