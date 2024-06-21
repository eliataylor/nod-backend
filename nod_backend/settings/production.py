from .base import *
import os
from google.oauth2 import service_account


DEBUG = False

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
SECRET_KEY = os.environ["SECRET_KEY"]
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Set HSTS headers
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to all subdomains
SECURE_HSTS_PRELOAD = True  # Allow the site to be included in browsers' HSTS preload list


# Google Cloud Storage settings
GS_BUCKET_NAME = 'nod_media'
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, 'path/to/your-service-account-file.json')
)

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_DEFAULT_ACL = 'publicRead'

MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'

try:
    from .local import *
except ImportError:
    pass
