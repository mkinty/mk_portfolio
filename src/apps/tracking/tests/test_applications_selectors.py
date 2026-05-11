import pytest

from apps.tracking.models import ApplicationStatus
from apps.tracking.selectors.applications_selectors import (
    ApplicationSelectors,
    FollowUpSelectors
)


# =========================================================
# ApplicationSelectors
# =========================================================

@pytest.mark.django_db
class TestApplicationSelectors:

    def test_get_application_by_id(self, job_application):
        result = ApplicationSelectors.get_application_by_id(job_application.id)

        assert result is not None
        assert result.id == job_application.id

    def test_get_application_by_id_returns_none(self):
        result = ApplicationSelectors.get_application_by_id(999999)

        assert result is None

    def test_get_application_by_user(
            self,
            user,
            job_application,
            job_application_with_status
    ):
        results = ApplicationSelectors.get_application_by_user(user)

        assert results.count() == 2
        assert job_application in results
        assert job_application_with_status in results

    def test_get_application_by_status(self, job_application_with_status):
        results = ApplicationSelectors.get_application_by_status(
            ApplicationStatus.INTERVIEWING
        )

        assert job_application_with_status in results

    def test_get_all_applications(
            self,
            job_application,
            job_application_with_status
    ):
        results = ApplicationSelectors.get_all_applications()

        assert results.count() >= 2
        assert job_application in results
        assert job_application_with_status in results


# =========================================================
# FollowUpSelectors
# =========================================================

@pytest.mark.django_db
class TestFollowUpSelectors:

    def test_get_follow_ups_by_application(
            self,
            job_application,
            follow_up,
            follow_up_completed
    ):
        results = FollowUpSelectors.get_follow_ups_by_application(
            job_application
        )

        assert follow_up in results
        assert follow_up_completed in results
        assert results.count() == 2
