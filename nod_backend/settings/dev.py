from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

INSTALLED_APPS += [
    'django_extensions',  # Example of a dev-only app
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1:8000",
    "127.0.0.1",
    "*.a.run.app",
    "nod-django-app-7z6iwfp5aa-uw.a.run.app",
    "https://nourishmentondemand.com",
    "https://www.nourishmentondemand.com",
]

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

try:
    from .local import *
except ImportError:
    pass
