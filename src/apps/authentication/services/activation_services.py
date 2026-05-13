from typing import Optional

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.authentication.services.token_services import generate_reset_token
from apps.notifications.services.email_service import send_email
from apps.users.models import User


def send_user_activation_email(user: Optional[User], domain: str) -> None:
    """
    Send an account activation email to a newly registered user.

    This function generates a unique activation link using the user's ID
    (encoded in base64) and a secure token. It then sends an email
    containing the activation link to the user's registered email address.

    Args:
        user Optional[User]: The user instance to activate.
        domain (str): The domain of the website, used to build the activation link.
            Example: "https://example.com"

    Returns:
        None

    Example:
        send_user_activation_email(user, "https://mywebsite.com")
        :param user: user
        :param domain: "https://mywebsite.com"
    """
    # Encode the user's primary key to safely include it in the URL
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Generate a secure token for account activation
    token = generate_reset_token(user)

    # Build the full activation link
    activation_link = f"{domain}/auth/activate/{uid}/{token}/"

    # Send the activation email using the notifications service
    send_email(
        subject="Activation de votre compte",
        message=f"Activez votre compte : {activation_link}",
        recipients=["kintymoustapha@gmail.com"],
        # You can replace this with [user.email] to send
        # the email to the currently logged-in user
    )
