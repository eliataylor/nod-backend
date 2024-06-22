from .base import *
import os

DEBUG = False

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = [
    "*.a.run.app"
]

# Set HSTS headers
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to all subdomains
SECURE_HSTS_PRELOAD = True  # Allow the site to be included in browsers' HSTS preload list

# Define static storage via django-storages[google]
GS_BUCKET_NAME = os.getenv('GCP_BUCKET_NAME')
GS_CREDENTIALS = os.getenv('GCP_SA_KEY')
STATIC_URL = "/static/"
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"

# Define MySQL database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "HOST": os.getenv("MYSQL_INSTANCE"),
        "PORT": "3306",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#     }
# }


# Superuser creation settings
SUPERUSER_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME')
SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD')
SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL')

try:
    from .local import *
except ImportError:
    pass
