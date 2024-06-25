from django.contrib.auth import get_user_model

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
    body_data = {
        "subject": "The user was trying to sign up",
        "recipients": [admin_email],
        "type": "html",
        "template_name": "user/notify_admin_that_user_wanted_to_signup.html",
        "template_body": {
            "user_email": user_email,
        },
    }
    # brm_api_client.send_email(body_data)
    return "notify_admin_that_user_wanted_to_signup"