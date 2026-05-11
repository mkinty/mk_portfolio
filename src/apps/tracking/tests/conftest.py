import pytest
from datetime import date
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.tracking.models import (
    JobApplication,
    ApplicationFollowUp,
    ApplicationStatus,
    FollowUpStatus,
)
from apps.users.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="testpass123"
    )


@pytest.fixture
def job_application(db, user):
    return JobApplication.objects.create(
        user=user,
        position="Backend Developer",
        company="OpenAI",
        job_offer_link="https://openai.com",
        resume=SimpleUploadedFile("cv.pdf", b"fake-cv-content"),
        application_date=date(2024, 1, 1),
    )


@pytest.fixture
def job_application_with_status(db, user):
    return JobApplication.objects.create(
        user=user,
        position="Data Engineer",
        company="Google",
        resume=SimpleUploadedFile("cv.pdf", b"fake-cv-content"),
        application_date=date(2024, 2, 1),
        application_status=ApplicationStatus.INTERVIEWING,
    )


@pytest.fixture
def follow_up(db, job_application):
    return ApplicationFollowUp.objects.create(
        job_application=job_application,
        title="Premier entretien RH",
        date=timezone.now(),
    )


@pytest.fixture
def follow_up_completed(db, job_application):
    return ApplicationFollowUp.objects.create(
        job_application=job_application,
        title="Entretien technique",
        date=timezone.now(),
        status=FollowUpStatus.COMPLETED,
    )