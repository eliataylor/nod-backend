from .base import *
import os
from google.oauth2 import service_account


DEBUG = False

CORS_ALLOWED_ORIGINS = [
    "https://nourishmentondemand.com",
    "https://www.nourishmentondemand.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
SECRET_KEY = "uqI9nmzRlaqoYMApQhxpgbLJfGFwPiWmMOHxKbqTYydHqeRXMp"
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Set HSTS headers
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to all subdomains
SECURE_HSTS_PRELOAD = True  # Allow the site to be included in browsers' HSTS preload list


GS_CREDENTIALS = os.environ['GCP_SA_KEY']

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_DEFAULT_ACL = 'publicRead'

MEDIA_URL = f'https://storage.googleapis.com/{os.environ["GCP_BUCKET_NAME"]}/'

""""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["MYSQL_DB"],
        "USER": os.environ["MYSQL_USER"],
        "PASSWORD": os.environ["MYSQL_PASS"],
        "HOST": os.environ["MYSQL_HOST"],
        "PORT": "3306",
    }
}
"""

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
