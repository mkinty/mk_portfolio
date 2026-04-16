from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from config.settings import settings


# Create your models here.


class UserProfile(models.Model):
    """
    Additional profile information linked to a user.

    This model stores optional metadata related to a user such as
    professional title, position, avatar, and biography content.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="The user associated with this profile."
    )
    title = models.CharField(
        max_length=150,
        blank=True,
        help_text="Professional title of the user (e.g., Software Engineer)."
    )
    position = models.CharField(
        max_length=150,
        blank=True,
        help_text="Current position or role held by the user."
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        help_text="Profile picture of the user."
    )
    bio = CKEditor5Field(
        "Content",
        config_name="default",
        blank=True,
        help_text="Detailed biography or description of the user."
    )

    def __str__(self):
        """
        Return the string representation of the user profile.

        Returns:
            str: A formatted string containing the related user.
        """
        return f"Profil de {self.user}"
