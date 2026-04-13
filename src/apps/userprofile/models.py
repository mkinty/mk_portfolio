from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from config.settings import settings


# Create your models here.


class UserProfile(models.Model):
    """
    Additional profile information linked to a User.

    This model stores optional user metadata such as title,
    position, avatar, and biography.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    title = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    bio = CKEditor5Field("Content", config_name="extends", blank=True)

    def __str__(self):
        """
        Return the string representation of the user profile.

        Returns:
            str: The related user's string representation.
        """
        return f"Profil de {self.user}"
