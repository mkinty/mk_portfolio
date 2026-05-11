import pytest
from apps.tracking.models import (
    JobApplication,
    ApplicationStatus,
    ApplicationFollowUp,
    FollowUpStatus,
)


@pytest.mark.django_db
class TestJobApplicationModel:
    """Test suite for the JobApplication model"""

    def test_create_job_application(self, job_application, user):
        """Test that job_application was created"""
        assert job_application.id is not None
        assert job_application.position == "Backend Developer"
        assert job_application.company == "OpenAI"
        assert job_application.application_status == ApplicationStatus.SENT

    def test_str_method(self, job_application):
        assert str(job_application) == "Backend Developer - OpenAI"

    def test_default_status(self, user):
        job = JobApplication.objects.create(
            user=user,
            position="Dev",
            company="TestCorp",
            resume="resumes/cv.pdf",
            application_date="2024-01-01",
        )
        assert job.application_status == ApplicationStatus.SENT

    def test_optional_fields(self, job_application):
        assert job_application.job_offer_link == "https://openai.com"
        assert not job_application.job_offer_file.name
        assert not job_application.cover_letter.name

    def test_ordering(self, user):
        old = JobApplication.objects.create(
            user=user,
            position="Old",
            company="A",
            resume="resumes/cv.pdf",
            application_date="2023-01-01",
        )

        new = JobApplication.objects.create(
            user=user,
            position="New",
            company="B",
            resume="resumes/cv.pdf",
            application_date="2024-01-01",
        )

        jobs = JobApplication.objects.all()
        assert jobs[0] == new
        assert jobs[1] == old

    def test_meta_verbose_name(self):
        assert JobApplication._meta.verbose_name == "Candidature"

    def test_meta_verbose_name_plural(self):
        assert JobApplication._meta.verbose_name_plural == "Candidatures"


@pytest.mark.django_db
class TestApplicationFollowUpModel:

    def test_create_follow_up(self, follow_up, job_application):
        assert follow_up.id is not None
        assert follow_up.job_application == job_application
        assert follow_up.title == "Premier entretien RH"
        assert follow_up.status == FollowUpStatus.PENDING

    def test_str_method(self, follow_up):
        assert str(follow_up) == follow_up.title

    def test_default_status(self, job_application):
        follow = ApplicationFollowUp.objects.create(
            job_application=job_application,
            title="Test",
            date="2024-01-01T10:00:00Z",
        )
        assert follow.status == FollowUpStatus.PENDING

    def test_status_completed(self, follow_up_completed):
        assert follow_up_completed.status == FollowUpStatus.COMPLETED

    def test_relationship_with_job_application(self, follow_up, job_application):
        assert follow_up.job_application == job_application
        assert follow_up in job_application.follow_ups.all()

    def test_ordering(self):
        assert ApplicationFollowUp._meta.ordering == ["date"]

    def test_meta_verbose_name(self):
        assert ApplicationFollowUp._meta.verbose_name == "Élément de suivi"

    def test_meta_verbose_name_plural(self):
        assert ApplicationFollowUp._meta.verbose_name_plural == "Éléments de suivi"
