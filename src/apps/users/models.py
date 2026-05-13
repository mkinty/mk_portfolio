from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user manager where email is used as the unique identifier
    instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.

        Args:
            email (str): The user's email address.
            password (str, optional): The user's password.
            **extra_fields: Additional fields for the user model.

        Returns:
            User: The created user instance.

        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with administrative privileges.

        Args:
            email (str): The user's email address.
            password (str, optional): The user's password.
            **extra_fields: Additional fields for the user model.

        Returns:
            User: The created superuser instance.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model that replaces username with email as the unique identifier.

    This model extends Django's AbstractUser and removes the username field.
    Email is used for authentication instead.
    """

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    # Override default relations to avoid conflicts with auth.User
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        """
        Return the string representation of the user.

        Returns:
            str: Full name if available, otherwise email.
        """
        return self.get_full_name().strip() or self.email
