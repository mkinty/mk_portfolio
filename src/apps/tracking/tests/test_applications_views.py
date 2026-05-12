import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.tracking.models import (
    JobApplication,
    ApplicationFollowUp,
    ApplicationStatus,
    FollowUpStatus,
)


# =========================================================
# ApplicationsTrackingIndexView
# =========================================================

@pytest.mark.django_db
class TestApplicationsTrackingIndexView:

    def test_get(self, client, user):
        url = reverse(
            "tracking:applications-index",
            kwargs={"user_id": user.id}
        )

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["user_obj"] == user
        assert "status" in response.context


# =========================================================
# ApplicationsTrackingView
# =========================================================

@pytest.mark.django_db
class TestApplicationsTrackingView:

    def test_get(self, client, user, job_application):
        url = reverse(
            "tracking:applications-tracking",
            kwargs={"user_id": user.id}
        )

        response = client.get(url)

        assert response.status_code == 200
        assert job_application in response.context["applications"]

    def test_filter_by_status(
            self,
            client,
            user,
            job_application_with_status
    ):
        url = reverse(
            "tracking:applications-tracking",
            kwargs={"user_id": user.id}
        )

        response = client.get(url, {
            "status": [ApplicationStatus.INTERVIEWING]
        })

        applications = response.context["applications"]

        assert response.status_code == 200
        assert job_application_with_status in applications

    def test_search_query(
            self,
            client,
            user,
            job_application
    ):
        url = reverse(
            "tracking:applications-tracking",
            kwargs={"user_id": user.id}
        )

        response = client.get(url, {
            "qs": "Backend"
        })

        applications = response.context["applications"]

        assert response.status_code == 200
        assert job_application in applications


# =========================================================
# JobApplicationAddView
# =========================================================

@pytest.mark.django_db
class TestJobApplicationAddView:

    def test_get(self, client, user):
        url = reverse(
            "tracking:add-application",
            kwargs={"user_id": user.id}
        )

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["title"] == "Ajouter une candidature"

    def test_post_valid(self, client, user):
        url = reverse(
            "tracking:add-application",
            kwargs={"user_id": user.id}
        )

        response = client.post(
            url,
            data={
                "position": "DevOps Engineer",
                "company": "Amazon",
                "job_offer_link": "https://amazon.com",
                "application_date": "2024-01-01",
                "application_status": ApplicationStatus.SENT,
                "resume": SimpleUploadedFile(
                    "cv.pdf",
                    b"fake-content"
                ),
            }
        )

        assert response.status_code == 200
        assert JobApplication.objects.count() == 1

    def test_post_invalid(self, client, user):
        url = reverse(
            "tracking:add-application",
            kwargs={"user_id": user.id}
        )

        response = client.post(url, data={})

        assert response.status_code == 200
        assert "form" in response.context


# =========================================================
# JobApplicationUpdateView
# =========================================================

@pytest.mark.django_db
class TestJobApplicationUpdateView:

    def test_get(self, client, job_application):
        url = reverse(
            "tracking:update-application",
            kwargs={"application_id": job_application.id}
        )

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["title"] == "Modifier une candidature"

    def test_post_valid(self, client, job_application):
        url = reverse(
            "tracking:update-application",
            kwargs={"application_id": job_application.id}
        )

        response = client.post(
            url,
            data={
                "position": "Updated Position",
                "company": "OpenAI",
                "application_date": "2024-01-01",
                "application_status": ApplicationStatus.SENT,
            }
        )

        job_application.refresh_from_db()

        assert response.status_code == 200
        assert job_application.position == "Updated Position"


# =========================================================
# ApplicationStatusUpdateView
# =========================================================

@pytest.mark.django_db
class TestApplicationStatusUpdateView:

    def test_get(self, client, job_application):
        url = reverse(
            "tracking:update-application-status",
            kwargs={"application_id": job_application.id}
        )

        response = client.get(url)

        assert response.status_code == 200
        assert response.context["title"] == "Modifier l'état"


# =========================================================
# JobApplicationDeleteView
# =========================================================

@pytest.mark.django_db
class TestJobApplicationDeleteView:

    def test_get(self, client, job_application):
        url = reverse(
            "tracking:delete-application",
            kwargs={"application_id": job_application.id}
        )

        response = client.get(url)

        assert response.status_code == 200

    def test_post(self, client, job_application):
        url = reverse(
            "tracking:delete-application",
            kwargs={"application_id": job_application.id}
        )

        response = client.post(url)

        assert response.status_code == 200
        assert JobApplication.objects.count() == 0


# =========================================================
# ApplicationFollowUpAddView
# =========================================================

@pytest.mark.django_db
class TestApplicationFollowUpAddView:

    def test_get(self, client, job_application):
        url = reverse(
            "tracking:add-followup",
            kwargs={"application_id": job_application.id}
        )

        response = client.get(url)

        assert response.status_code == 200

    def test_post_valid(self, client, job_application):
        url = reverse(
            "tracking:add-followup",
            kwargs={"application_id": job_application.id}
        )

        response = client.post(
            url,
            data={
                "title": "RH Interview",
                "event_date": "2024-01-01",
                "status": FollowUpStatus.PENDING,
            }
        )

        assert response.status_code == 200
        assert ApplicationFollowUp.objects.count() == 1


# =========================================================
# ApplicationFollowUpUpdateView
# =========================================================

@pytest.mark.django_db
class TestApplicationFollowUpUpdateView:

    def test_get(self, client, follow_up):
        url = reverse(
            "tracking:update-followup",
            kwargs={"followup_id": follow_up.id}
        )

        response = client.get(url)

        assert response.status_code == 200

    def test_post_valid(self, client, follow_up):
        url = reverse(
            "tracking:update-followup",
            kwargs={"followup_id": follow_up.id}
        )

        response = client.post(
            url,
            data={
                "title": "Updated Follow Up",
                "event_date": "2024-01-01",
                "status": FollowUpStatus.COMPLETED,
            }
        )

        follow_up.refresh_from_db()

        assert response.status_code == 200
        assert follow_up.title == "Updated Follow Up"


# =========================================================
# ApplicationFollowUpDeleteView
# =========================================================

@pytest.mark.django_db
class TestApplicationFollowUpDeleteView:

    def test_get(self, client, follow_up):
        url = reverse(
            "tracking:delete-followup",
            kwargs={"followup_id": follow_up.id}
        )

        response = client.get(url)

        assert response.status_code == 200

    def test_post(self, client, follow_up):
        url = reverse(
            "tracking:delete-followup",
            kwargs={"followup_id": follow_up.id}
        )

        response = client.post(url)

        assert response.status_code == 200
        assert ApplicationFollowUp.objects.count() == 0
