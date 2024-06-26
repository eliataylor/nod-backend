from .base import *

DEBUG = os.getenv('DJANGO_DEBUG', 'False')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Set HSTS headers
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to all subdomains
SECURE_HSTS_PRELOAD = True  # Allow the site to be included in browsers' HSTS preload list
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Define static storage via django-storages[google]
# Using default Cloud Run service account
# GS_CREDENTIALS = os.getenv('GCP_SA_KEY')
GS_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
GS_BUCKET_NAME = os.getenv('GCP_BUCKET_NAME')
STATIC_URL = "/static/"
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"


SPECTACULAR_SETTINGS = {
    "SERVE_PUBLIC" : False,
    "SERVE_INCLUDE_SCHEMA" : False
}