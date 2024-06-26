from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from nod_backend.settings import (
    ADMIN_EMAIL,
    DEFAULT_FROM_EMAIL,
    REGISTRATION_BASED_ON_DOMAINS,
)

from .models import AvailableDomain


def check_if_domain_allowed(user_email):
    if not REGISTRATION_BASED_ON_DOMAINS:
        return True
    domain = user_email.split("@")[1]
    return AvailableDomain.objects.filter(name=domain).exists()

def notify_admin_that_user_wanted_to_signup(user_email):
    admin_email = ADMIN_EMAIL or DEFAULT_FROM_EMAIL

    send_mail(
        'Subject here',
        f'{user_email} wants to sign up',
        admin_email,
        [user_email],
        fail_silently=False,
    )

    return "notify_admin_that_user_wanted_to_signup"