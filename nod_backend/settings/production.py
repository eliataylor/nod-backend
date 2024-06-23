from .base import *

DEBUG = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Set HSTS headers
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to all subdomains
SECURE_HSTS_PRELOAD = True  # Allow the site to be included in browsers' HSTS preload list

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',')

# Define static storage via django-storages[google]
# Using default Cloud Run service account
# GS_CREDENTIALS = os.getenv('GCP_SA_KEY')
GS_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
GS_BUCKET_NAME = os.getenv('GCP_BUCKET_NAME')
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
        "HOST": os.getenv("MYSQL_HOST")
    }
}

# try:
#     from .local import *
# except ImportError:
#     pass

print(f"Production setting (production.py) is Loaded")