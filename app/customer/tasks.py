from django.core.mail import send_mail
from celery import shared_task
from main_vars import vars

@shared_task
def send_email_code(email,random_digit):
    send_mail(
        'Confirmation email code',
        f'Hello your confirmation code - {random_digit}\nEnter it in code field',
        vars.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )