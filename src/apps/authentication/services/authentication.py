from typing import Optional

from django.contrib.auth import authenticate, login
from apps.users.models import User


def authenticate_user(email: str, password: str) -> Optional[User]:
    """
    Authenticate a user using email and password.

    This function relies on Django's authentication system, which will
    automatically use the configured authentication backend
    (EmailBackend in this case).

    Args:
        email (str): User email address.
        password (str): Raw password.

    Returns:
        Optional[User]: Authenticated user instance or None.
    """
    return authenticate(email=email, password=password)