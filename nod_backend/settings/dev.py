from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure--9&$hhrd-c!#$r)^on)uvz7x^4pdhel_e4uefy+dhf9k3shfm^"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
#     os.path.join(BASE_DIR, os.getenv('GCP_SA_KEY'))
# )

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

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": os.getenv("MYSQL_DATABASE"),
#         "USER": os.getenv("MYSQL_USER"),
#         "PASSWORD": os.getenv("MYSQL_PASSWORD"),
#         "HOST": "127.0.0.1",
#         "PORT": "3306",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

try:
    from .local import *
except ImportError:
    pass
