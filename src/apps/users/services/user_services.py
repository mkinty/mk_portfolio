from typing import Optional

from apps.users.models import User


def create_user_account(first_name: str, last_name: str, email: str, password: str) -> Optional[User]:
    """
    Create a new inactive user account.

    The account is created inactive to require email activation.

    Args:
        first_name (str): User first name.
        last_name (str): User last name.
        email (str): User email address.
        password (str): Raw password (hashed automatically).

    Returns:
        Optional[User]: Created inactive user instance.
    """
    user = User.objects.create_user(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
    )
    user.is_active = False
    user.save()
    return user


def activate_user_account(user):
    """
    Activate a user account by enabling it and clearing the activation token.

    Args:
        user (User): The user instance to activate.

    Returns:
        None

    Notes:
        - Sets `is_active` to True to allow the user to log in.
        - Clears the `activation_token` to prevent reuse.
        - Saves the changes to the database immediately.
    """
    user.is_active = True
    user.activation_token = None
    user.save()


def set_user_password(user, password):
    """
    Set a new password for a user and save it to the database.

    Args:
        user (User): The user instance whose password will be set.
        password (str): The new plaintext password to set.

    Returns:
        None

    Notes:
        - Uses Django's `set_password` method to securely hash the password.
        - Saves the user instance to persist the new password.
    """
    user.set_password(password)
    user.save()
