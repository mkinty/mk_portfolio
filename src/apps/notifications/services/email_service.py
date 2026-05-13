from django.conf import settings

from ..tasks import send_email_task


def send_email(subject: str, message: str, recipients: list[str]) -> None:
    """
    Send an email asynchronously using Celery.

    This function schedules a Celery task (`send_email_task`) to send an email
    with the specified subject and message to the list of recipients. The sender
    email is automatically taken from Django's `EMAIL_HOST_USER` setting.

    Args:
        subject (str): The subject line of the email.
        message (str): The body of the email.
        recipients (list[str]): A list of recipient email addresses.

    Returns:
        None

    Example:
        send_activation_email(
            subject="Activate your account",
            message="Click this link to activate your account...",
            recipients=["user@example.com"]
        )
    """
    send_email_task.delay(subject, message, settings.EMAIL_HOST_USER, recipients)
