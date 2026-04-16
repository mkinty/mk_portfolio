from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from config.settings import settings


# Create your models here.


class EducationSection(models.Model):
    """
    Represents an introduction section for the academic background.

    This model is used to display a title and description
    before listing education entries.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="education_sections",
        help_text="Utilisateur associé à cette section académique."
    )

    name = models.CharField(
        max_length=150,
        help_text="Titre de la section (ex: Parcours Académique)."
    )

    description = CKEditor5Field(
        "Content",
        config_name="default",
        blank=True,
        help_text="Description introductive du parcours académique."
    )

    def __str__(self):
        """
        Return the string representation of the section.

        Returns:
            str: Section name.
        """
        return self.name


class Education(models.Model):
    """
    Education background entry linked to an EducationSection.

    This model stores academic records such as school, degree,
    field of study, and dates.
    """

    education_section = models.ForeignKey(
        EducationSection,
        on_delete=models.CASCADE,
        related_name="educations",
        help_text="Section académique à laquelle cette formation appartient."
    )

    school = models.CharField(
        max_length=150,
        help_text="Nom de l'établissement (ex: Université de Paris)."
    )

    degree = models.CharField(
        max_length=150,
        help_text="Diplôme obtenu (ex: Licence, Master, Doctorat)."
    )

    field_of_study = models.CharField(
        max_length=150,
        blank=True,
        help_text="Domaine d'étude (ex: Informatique, Mathématiques)."
    )

    start_date = models.DateField(
        help_text="Date de début de la formation."
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date de fin de la formation (laisser vide si en cours)."
    )

    description = CKEditor5Field(
        "Content",
        config_name="default",
        blank=True,
        help_text="Description optionnelle (résultats, projets, mentions, etc.)."
    )

    def __str__(self):
        """
        Return the string representation of the education entry.
        """
        return f"{self.degree} - {self.school}"
