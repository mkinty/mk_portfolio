from django.db import models

from config.settings import settings


# Create your models here.


class TechStackCategory(models.Model):
    """
    Represents a category of technologies (Frontend, Backend, DevOps...).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tech_stack_categories",
        help_text="Utilisateur propriétaire des catégories."
    )

    name = models.CharField(
        max_length=100,
        help_text="Nom de la catégorie (ex: Backend, Frontend)."
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text="Ordre d'affichage."
    )

    class Meta:
        ordering = ["order"]
        unique_together = ("user", "name")

    def __str__(self):
        return self.name


class TechStack(models.Model):
    """
    Represents a technology inside a category.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tech_stacks",
    )

    category = models.ForeignKey(
        TechStackCategory,
        on_delete=models.CASCADE,
        related_name="techs",
        help_text="Catégorie associée."
    )

    name = models.CharField(
        max_length=100,
        help_text="Nom de la technologie (ex: Django, React)."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "name"]
        unique_together = ("user", "name")

    def __str__(self):
        return self.name
