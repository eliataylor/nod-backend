from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--9&$hhrd-c!#$r)^on)uvz7x^4pdhel_e4uefy+dhf9k3shfm^"

# SECURITY WARNING: define the correct hosts in production!
CORS_ALLOWED_ORIGINS = [
    "https://nourishmentondemand.com",
    "https://www.nourishmentondemand.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# ALLOWED_HOSTS = ["*"]
# CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
