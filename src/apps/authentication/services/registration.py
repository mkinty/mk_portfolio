from typing import List, Optional

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from apps.authentication.services.activation import send_user_activation_email
from apps.users.models import User
from apps.users.selectors.user import user_exists_by_email
from apps.users.services.user import create_user_account


def validate_registration_data(
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        password2: str) -> List[str]:
    """
    Validate user registration input data.

    Checks for:
    - Presence and validity of email
    - Uniqueness of email
    - Password length (minimum 6 characters)
    - Password confirmation match

    Args:
        first_name (str): User's first name.
        last_name (str): User's last name.
        email (str): The user's email address.
        password (str): The user's chosen password.
        password2 (str): The password confirmation.

    Returns:
        List[str]: A list of error messages. Empty list if no errors.

    Example:
        errors = validate_registration_data("user@example.com", "pass123", "pass123")
        if errors:
            # handle errors
    """
    errors: List[str] = []
    if not first_name:
        errors.append("Merci de renseigner votre prénom")
    if not last_name:
        errors.append("Merci de renseigner votre nom")
    if not email:
        errors.append("Merci de renseigner votre adresse email")
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors.append("Merci d'entrer une adresse email valide")

    if user_exists_by_email(email):
        errors.append("Cette adresse email existe déjà")

    if len(password) < 6:
        errors.append("Les mots de passe doivent comporter au moins 6 caractères")

    if password != password2:
        errors.append("Les mots de passe ne correspondent pas")

    return errors


def register_user(first_name: str, last_name: str, email: str, password: str, domain: str) -> Optional[User]:
    """
    Create a new user account and send an activation email.

    This function handles:
    - Creating a new user with inactive status
    - Sending the activation email to the user's email address

    Args:
        first_name (str): User's first name.
        last_name (str): User's last name.
        email (str): User's email address.
        password (str): User's password.
        domain (str): The domain to use for constructing the activation link.

    Returns:
        Optional[User]: The newly created user instance.

    Example:
        user = register_user("John", "Doe", "john@example.com", "securePass123", "https://mydomain.com")
    """
    user = create_user_account(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    send_user_activation_email(user, domain)

    return user
