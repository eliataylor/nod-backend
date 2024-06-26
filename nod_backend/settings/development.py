from .base import *

INSTALLED_APPS += [
    'django_extensions',  # Example of a dev-only app
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

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

# try:
#     from .local import *
# except ImportError:
#     pass

print(f"Development setting (development.py) is Loaded")