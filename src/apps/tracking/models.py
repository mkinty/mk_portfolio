from django.db import models

from config.settings import settings
# Create your models here.


class ApplicationStatus(models.TextChoices):
    """Application status"""
    SENT = "Envoyée", "Envoyée"
    INTERVIEWING = "Entretiens en cours", "Entretiens en cours"
    ACCEPTED = "Acceptée", "Acceptée"
    REJECTED = "Rejetée", "Rejetée"


class JobApplication(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_applications",
        help_text="Utilisateur envoyant des candidatures."
    )

    position = models.CharField(
        max_length=255,
        help_text="Intitulé du poste"
    )

    company = models.CharField(
        max_length=255,
        help_text="Entreprise"
    )

    job_offer_link = models.URLField(
        blank=True,
        null=True,
        help_text="Lien vers l'offre"
    )

    job_offer_file = models.FileField(
        upload_to="job_offers/",
        blank=True,
        null=True,
        help_text="Offre sous format fichier"
    )

    resume = models.FileField(
        upload_to="resumes/",
        help_text="CV adapté à l'offre"
    )

    cover_letter = models.FileField(
        upload_to="cover_letters/",
        blank=True,
        null=True,
        help_text="Lettre de motivation adaptée à l'offre"
    )

    application_date = models.DateField(
        verbose_name="Date de candidature"
    )

    application_status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.SENT,
        help_text="État de la candidature"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date de mise à jour"
    )

    class Meta:
        ordering = ["-application_date"]
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"

    def __str__(self):
        return f"{self.position} - {self.company}"


class FollowUpStatus(models.TextChoices):
    PENDING = "En attente", "En attente"
    COMPLETED = "Terminé", "Terminé"
    CANCELLED = "Annulé", "Annulé"


class ApplicationFollowUp(models.Model):
    job_application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="follow_ups",
        verbose_name="Candidature",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Intitulé"
    )

    date = models.DateField(
        verbose_name="Date"
    )

    status = models.CharField(
        max_length=20,
        choices=FollowUpStatus.choices,
        default=FollowUpStatus.PENDING,
        verbose_name="Statut"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    class Meta:
        ordering = ["date"]
        verbose_name = "Élément de suivi"
        verbose_name_plural = "Éléments de suivi"

    def __str__(self):
        return self.title
