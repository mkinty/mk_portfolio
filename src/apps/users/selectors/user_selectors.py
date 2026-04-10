from typing import Optional

from django.utils.http import urlsafe_base64_decode

from apps.authentication.services.token_services import verify_token
from apps.users.models import User


def get_all_users():
    """
    Retrieve all users.

    Returns:
        QuerySet[User]: Django QuerySet containing all users.
    """
    return User.objects.all()


def get_user_by_id(user_id: int):
    """
    Retrieve a user by its unique identifier.

    Args:
        user_id (int): ID of the user.

    Returns:
        User | None: The user instance if found, otherwise None.
    """
    return User.objects.filter(id=user_id).first()


def get_user_by_email(email: str) -> Optional[User] | None:
    """
    Retrieve a user by email address.

    Args:
        email (str): Email address of the user.

    Returns:
        Optional[User] | None: The user instance if found, otherwise None.
    """
    return User.objects.filter(email=email).first()


def get_user_by_activation_token(token: str) -> Optional[User] | None:
    """
    Retrieve a user instance associated with a given activation token.

    Args:
        token (str): The activation token assigned to a user.

    Returns:
        Optional[User] or None: Returns the User object if found, otherwise None.

    Notes:
        - This function queries the database for a user whose `activation_token`
          matches the provided token.
        - If multiple users somehow have the same token (should not happen),
          only the first match is returned.
    """
    return User.objects.filter(activation_token=token).first()


def get_user_from_token(uidb64: str, token: str) -> Optional[User]:
    """
    Retrieve a User instance by decoding a base64-encoded user ID and verifying a password reset token.

    This function is typically used in password reset flows. It decodes the provided `uidb64`
    parameter to obtain the user's primary key, fetches the corresponding `User` from the database,
    and then validates the provided token using `verify_token`.

    Args:
        uidb64 (str): Base64-encoded string representing the user's ID.
        token (str): The password reset token to verify.

    Returns:
        Optional[User]: The `User` instance if the token is valid and the user exists; otherwise, `None`.

    Notes:
        - Returns `None` if the decoding fails, the user does not exist, or the token is invalid.
        - Depends on `urlsafe_base64_decode` from `django.utils.http` and `verify_token` from your authentication services.

    Example:
        >>  user = get_user_from_token('Mg==', 'some-token')
        >>  if user:
        ...     print(user.email)
        ... else:
        ...     print("Invalid token or user does not exist")
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None

    if not verify_token(user, token):
        return None
    return user


def user_exists_by_email(email: str) -> bool:
    """
    Check if a user exists with the given email.

    Args:
        email (str): Email address to check.

    Returns:
        bool: True if a user exists with this email, otherwise False.
    """
    return User.objects.filter(email=email).exists()
