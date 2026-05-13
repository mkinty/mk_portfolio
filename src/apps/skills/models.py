from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from config.settings import settings


class Skills(models.Model):
    """
    Represents a technical or professional skill associated with a user.

    This model stores skills that a user has acquired,
    along with an optional rich-text description.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="skills",
        help_text="The user who owns this skill.",
    )

    name = models.CharField(
        max_length=150,
        help_text="The skills category name (e.g., Programming Languages, Tools).",
    )

    description = CKEditor5Field(
        "Content",
        config_name="default",
        blank=True,
        help_text="Optional detailed description of the skill.",
    )

    def __str__(self) -> str:
        """
        Return the string representation of the skill.

        Returns:
            str: Name of the skill.
        """
        return self.name
