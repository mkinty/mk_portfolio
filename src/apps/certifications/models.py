from django.db import models

from config.settings import settings


# Create your models here.

class Certification(models.Model):
    """
    Model representing a certification earned by a user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="certifications",
        help_text="Utilisateur propriétaire de la certification"
    )
    name = models.CharField(
        max_length=255,
        help_text="Le nom de la certification"
    )
    issuer = models.CharField(
        max_length=255,
        blank=True,
        help_text="L'organisme qui a délivré la certification ou lien vers le certificat"
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
