from typing import Optional

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from apps.authentication.services.token import generate_reset_token
from apps.notifications.services.email_service import send_activation_email
from apps.users.models import User


def send_password_reset_email(user: Optional[User], domain: str) -> None:
    """
    Send a password reset email to a user who requested a password reset.

    This function generates a unique password reset link using the user's ID
    (encoded in base64) and a secure token. It then sends an email
    containing the reset link to the user's registered email address.

    Args:
        user (Optional[User]): The user instance requesting password reset.
        domain (str): The domain of the website, used to build the reset link.
            Example: "https://example.com"

    Returns:
        None

    Example:
        send_password_reset_email(user, "https://mywebsite.com")
        :param user: user
        :param domain: "https://mywebsite.com"
    """
    if not user:
        return

    # Encode the user's primary key to safely include it in the URL
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Generate a secure token for password reset
    token = generate_reset_token(user)

    # Build the full password reset link
    reset_link = f"{domain}/auth/password-reset/{uid}/{token}/"

    # Send the password reset email using the notifications service
    send_activation_email(
        subject="Réinitialisation de votre mot de passe",
        message=f"Hello {user.first_name},\nRéinitialiser votre mot de passe ici: {reset_link}",
        recipients=[user.email],
    )
