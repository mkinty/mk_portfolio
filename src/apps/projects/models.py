from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from config.settings import settings


# Create your models here.


class ProjectCategory(models.Model):
    """
    Catégorie de projet
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_categories",
        help_text="Utilisateur propriétaire des catégories de projets."
    )
    name = models.CharField(
        max_length=100,
        help_text="Nom de la catégorie de projet."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de création de la catégorie."
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_projects",
        help_text="Utilisateur propriétaire des projets."
    )
    title = models.CharField(
        max_length=200,
        help_text="Nom du projet."
    )
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    start_date = models.DateField(
        help_text="Date de debut du projet"
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date de fin du projet"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Statut du projet (actif/inactif)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de création du projet"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date de dernière mise à jour du projet"
    )
    source_code_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL du code source du projet"
    )
    image = models.ImageField(
        upload_to='projects/images/',
        blank=True,
        null=True,
        help_text="Image du projet"
    )
    description = CKEditor5Field(
        "Content",
        config_name="default",
        blank=True,
        help_text="Détails complets du projet."
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
