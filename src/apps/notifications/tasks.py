from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    email = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list
    )
    email.send()
