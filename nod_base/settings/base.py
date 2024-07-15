import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '2BE830C1-C43C-41C5-952A-795720941B57')

DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

SUPERUSER_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME', 'superadmin')
SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin')
SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL', 'eli@taylormadetraffic.com')

ALLOWED_HOSTS = [
    "nourishmentondemand",
    ".nourishmentondemand",
    "nod-django-app-cloudrun-zzv45b5nya-uw.a.run.app",
    "prod_app.storage.googleapis.com"
]

CSRF_TRUSTED_ORIGINS = [
    "https://nod-django-app-cloudrun-zzv45b5nya-uw.a.run.app",
    "https://prod_app.storage.googleapis.com"
    "https://nourishmentondemand",
    "https://*.nourishmentondemand",
]

from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    'x-email-verification-key',  # used by allauth
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.nourishmentondemand\.com$",
    r"^http://\w+\.nourishmentondemand\.com$",
]
CORS_ALLOWED_ORIGINS = [
    'https://nourishmentondemand',
    'https://www.nourishmentondemand',
    'https://dev.nourishmentondemand',
    "https://nod-django-app-cloudrun-zzv45b5nya-uw.a.run.app",
    "https://prod_app.storage.googleapis.com"
]

CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read the CSRF cookie

SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = False  # Allow JavaScript to read the CSRF cookie

CORS_ALLOW_CREDENTIALS = True

# CSRF_TRUSTED_ORIGINS += CORS_ALLOWED_ORIGINS
# CSRF_COOKIE_NAME = "nod-jwt"

# JWT_AUTH_COOKIE = "nod-jwt"
# JWT_AUTH_REFRESH_COOKIE = "nod-refresh-jwt"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    'django.contrib.sessions',
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.humanize',
    'storages',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    "allauth",
    "allauth.account",

    "allauth.socialaccount",
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',
    "allauth.headless",
    "allauth.usersessions",

    'drf_spectacular',

    'djmoney',
    'nod_app',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #    'csp.middleware.CSPMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

GOOGLE_CALLBACK_URL = os.environ.get('GOOGLE_CALLBACK_URL', "")
CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', "")
SECRET = os.environ.get('GOOGLE_OAUTH_SECRET', "")
KEY = os.environ.get('GOOGLE_OAUTH_KEY', "")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}

SPECTACULAR_SETTINGS = {
    'TITLE': 'NOD',
    'DESCRIPTION': 'NourishmentOnDemand',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True
}

ROOT_URLCONF = 'nod_base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            #            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nod_base.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "HOST": os.getenv("MYSQL_HOST"),
        "PORT": 3306,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

GS_FILE_OVERWRITE = True  # WARN: change after initial launch!

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTH_USER_MODEL = "nod_app.Users"

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_LOGIN_BY_CODE_ENABLED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

HEADLESS_ONLY = True

FRONTEND_URL = os.environ.get("FRONT_END_URL", "https://localhost:3000")

HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": f"{FRONTEND_URL}/account/verify-email/{{key}}",
    # Key placeholders are automatically populated. You are free to adjust this to your own needs, e.g.
    "account_reset_password": f"{FRONTEND_URL}/account/password/reset",
    "account_reset_password_from_key": f"{FRONTEND_URL}/account/password/reset/key/{{key}}",
    "account_signup": f"{FRONTEND_URL}/account/signup",
    # Fallback in case the state containing the `next` URL is lost and the handshake
    # with the third-party provider fails.
    "socialaccount_login_error": f"{FRONTEND_URL}/account/provider/callback",
}

# ACCOUNT_ADAPTER = 'nod_app.adapter.UserAdapter'

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID', ""),
            'secret': os.environ.get('GOOGLE_OAUTH_SECRET', ""),
            'key': os.environ.get('GOOGLE_OAUTH_KEY', ""),
        },
        'FETCH_USERINFO': True,
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True
    }
}

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# SMTP server configuration
EMAIL_HOST = os.environ.get("SMTP_EMAIL_HOST", 'smtp.gmail.com')
EMAIL_PORT = os.environ.get("SMTP_EMAIL_PORT", 587)  # or 465 for SSL
EMAIL_USE_TLS = True  # or False for SSL
EMAIL_HOST_USER = os.environ.get("SMTP_EMAIL_ADDRESS", "")
EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "")
EMAIL_USE_LOCALTIME = True
# EMAIL_FILE_PATH = '/home/app-messages'  # change this to a proper location

TWILIO_AUTH_ACCOUNT_SID = os.environ.get("TWILIO_AUTH_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_VERIFY_SERVICE_SID = os.environ.get("TWILIO_VERIFY_SERVICE_SID", "")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER", "")
