from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--9&$hhrd-c!#$r)^on)uvz7x^4pdhel_e4uefy+dhf9k3shfm^"

CORS_ALLOWED_ORIGINS = [
    "https://nourishmentondemand.com",
    "https://www.nourishmentondemand.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

INSTALLED_APPS += [
    'django_extensions',  # Example of a dev-only app
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1:8000",
    "127.0.0.1"
]
# CORS_ALLOW_ALL_ORIGINS = True

try:
    from .local import *
except ImportError:
    pass
