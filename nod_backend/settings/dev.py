from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure--9&$hhrd-c!#$r)^on)uvz7x^4pdhel_e4uefy+dhf9k3shfm^"
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

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

# Default storage settings, with the staticfiles storage updated.
# See https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-STORAGES
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # ManifestStaticFilesStorage is recommended in production, to prevent
    # outdated JavaScript / CSS assets being served from cache
    # (e.g. after a Wagtail upgrade).
    # See https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

try:
    from .local import *
except ImportError:
    pass
