import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'm(##s4x5rs))6f09xu_xq@1a3-*5sm@n8bh^9dm(p46-%t@et%')

DEBUG = os.getenv('DJANGO_DEBUG', 'False')

# Superuser creation settings
SUPERUSER_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin')
SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL', 'eli@taylormadetraffic.com')

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', 'http://localhost,http://127.0.0.1').split(',')

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sessions',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'address',
    'djmoney',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'drf_spectacular',

    'users',
    'nod_app'
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
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MFA_FORMS = {
    'authenticate': 'allauth.mfa.forms.AuthenticateForm',
    'reauthenticate': 'allauth.mfa.forms.AuthenticateForm',
    'activate_totp': 'allauth.mfa.forms.ActivateTOTPForm',
    'deactivate_totp': 'allauth.mfa.forms.DeactivateTOTPForm',
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID', ""),
            'secret': os.environ.get('GOOGLE_OAUTH_SECRET', ""),
            'key': os.environ.get('GOOGLE_OAUTH_KEY', ""),
        },
    }
}

GOOGLE_CALLBACK_URL = os.environ.get('GOOGLE_CALLBACK_URL', "")
CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', "")
SECRET = os.environ.get('GOOGLE_OAUTH_SECRET', "")
KEY = os.environ.get('GOOGLE_OAUTH_KEY', "")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

ROOT_URLCONF = 'nod_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
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

WSGI_APPLICATION = 'nod_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "HOST": os.getenv("MYSQL_HOST")
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

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


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
#### needs to be tracked in Object actions:
DEFAULT_AUTO_FIELD='django.db.models.AutoField'
GOOGLE_API_KEY = 'CHANGEME'

GOOGLE_CALLBACK_URL = os.environ.get("GOOGLE_CALLBACK_URL", "")

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
FRONTEND_URL = os.environ.get("FRONT_END_URL", "https://localhost:3000")
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = FRONTEND_URL + "/verify-email" if FRONTEND_URL else "/"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = FRONTEND_URL + "/verify-email" if FRONTEND_URL else "/"
LOGIN_URL = FRONTEND_URL + "/auth/login"
LOGIN_REDIRECT_URL = FRONTEND_URL
ACCOUNT_PASSWORD_RESET_URL = FRONTEND_URL + "/auth/reset-password"
ACCOUNT_CONFIRM_EXPIRED_URL = FRONTEND_URL + "/auth/email-expired"
ACCOUNT_CONFIRM_EXPIRED_VERIFIED_URL = FRONTEND_URL + "/auth/email-verified"
REGISTRATION_BASED_ON_DOMAINS = os.environ.get("REGISTRATION_BASED_ON_DOMAINS", "False").lower() == "true"
FERNET_KEY = os.environ.get("FERNET_ENCRYPTION_KEY", "")

# Email Settings
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# SMTP server configuration
EMAIL_HOST = os.environ.get("SMTP_EMAIL_HOST", 'smtp.gmail.com')
EMAIL_PORT = os.environ.get("SMTP_EMAIL_PORT", 587)  # or 465 for SSL
EMAIL_USE_TLS = True  # or False for SSL
EMAIL_USE_SSL = False  # True if using SSL
EMAIL_HOST_USER = os.environ.get("SMTP_EMAIL_ADDRESS", "")
EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "")

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_LOCALTIME = True
EMAIL_FILE_PATH = '/home/app-messages'  # change this to a proper location

AUTH_USER_MODEL = "users.User"
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "users.serializers.UserSerializer",
    "PASSWORD_RESET_SERIALIZER": "users.serializers.CustomPasswordResetSerializer",
    "LOGIN_SERIALIZER": "users.serializers.CustomLoginSerializer",
}
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "users.serializers.UserRegistrationSerializer",
}
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'jwt-auth',
}
REST_USE_JWT = True
JWT_AUTH_COOKIE = "nod-backend-auth"
JWT_AUTH_REFRESH_COOKIE = "refreshToken"