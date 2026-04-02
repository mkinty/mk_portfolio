from typing import Optional

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from apps.users.models import User

token_generator = PasswordResetTokenGenerator()



def generate_reset_token(user: Optional[User]) -> str:
    """
    Generate a secure password reset token for the given user.

    This token can be sent via email to allow the user to reset their password.
    It is time-sensitive and linked to the user's state (password, last login, etc.)
    to prevent reuse of old tokens.

    Args:
        Optional[User]: The user instance for whom the reset token is generated.

    Returns:
        str: A secure token string that can be used for password reset URLs.

    Example:
        token = generate_reset_token(user)
        reset_link = f"https://example.com/reset-password/{user.pk}/{token}/"
    """
    return token_generator.make_token(user)



def verify_token(user: Optional[User], token: str) -> bool:
    """
    Verify the validity of a token for a given user.

    This function is typically used for:
    - Account activation links
    - Password reset links

    It checks if the token matches the user's current token state
    using Django's PasswordResetTokenGenerator or a custom token generator.

    Args:
        Optional[User]: The Django user instance for whom the token is being verified.
        token (str): The token string to validate.

    Returns:
        bool: True if the token is valid for the user, False otherwise.

    Example:
        if verify_token(user, token):
            # proceed with activation or password reset
            :param token:
            :param user:
        else:
            # handle invalid token

    """
    return token_generator.check_token(user, token)
