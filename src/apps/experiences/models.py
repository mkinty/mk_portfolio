from django.core.exceptions import ValidationError
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from config.settings import settings


class Experience(models.Model):
    """
    Professional experience associated with a user.

    This model stores information about a user's work experience,
    including job title, company, location, dates, and description.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="experiences",
        help_text="The user to whom this professional experience belongs.",
    )
    title = models.CharField(
        max_length=150, help_text="Job title or role held by the user."
    )
    company = models.CharField(
        max_length=150, help_text="Name of the company or organization."
    )
    location = models.CharField(
        max_length=150,
        blank=True,
        help_text="Location of the job (city, country, or remote).",
    )
    start_date = models.DateField(help_text="Start date of the experience.")
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="End date of the experience. Leave empty if ongoing.",
    )
    is_current = models.BooleanField(
        default=False,
        help_text="Indicates whether this position is the user's current job.",
    )
    description = CKEditor5Field(
        "Content",
        config_name="default",
        blank=True,
        help_text="Detailed description of responsibilities and achievements.",
    )

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("Date de fin doit être après la date de début.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        """
        Return the string representation of the experience.

        Returns:
            str: A formatted string containing title and company name.
        """
        return f"{self.title} - {self.company}"
