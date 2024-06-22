from .base import *

DEBUG = False

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = [
    "*.a.run.app",
    "https://nourishmentondemand.com",
    "https://www.nourishmentondemand.com"
]

# CORS_ALLOWED_ORIGINS = [
#     "https://nourishmentondemand.com",
#     "https://www.nourishmentondemand.com",
#     "https://*.nourishmentondemand.com",
#     "https://stage.nourishmentondemand.com",
#     "https://dev.nourishmentondemand.com",
#     "https://nod_django_prod.nourishmentondemand.com",
#     "https://nod-django-app-*.a.run.app",
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     "http://127.0.0.1:8000"
# ]

# CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# Set HSTS headers
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to all subdomains
SECURE_HSTS_PRELOAD = True  # Allow the site to be included in browsers' HSTS preload list

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
        "HOST": os.getenv("MYSQL_INSTANCE")
    }
}

try:
    from .local import *
except ImportError:
    pass
