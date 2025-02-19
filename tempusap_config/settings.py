"""
Django settings for Tempus Author Platform.

This module contains all the settings for the Tempus Author Platform project:

Key Settings:
- Security settings (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- Application definition and middleware configuration
- Database configuration with support for both SQLite and PostgreSQL
- Static and media files configuration with AWS S3 support
- Authentication settings using django-allauth
- Email configuration for both development and production
- Stripe payment integration settings
- Content Security Policy (CSP) configuration
- Custom settings for profile images and file uploads

Environment Variables:
- SECRET_KEY: Django secret key
- DATABASE_URL: Database connection URL (for production)
- AWS_ACCESS_KEY_ID: AWS access key for S3
- AWS_SECRET_ACCESS_KEY: AWS secret key for S3
- STRIPE_PUBLIC_KEY: Stripe publishable key
- STRIPE_SECRET_KEY: Stripe secret key
- EMAIL_HOST_USER: SMTP email user
- EMAIL_HOST_PASSWORD: SMTP email password
"""

import os
import dj_database_url
from django.contrib.messages import constants as messages
from pathlib import Path
if os.path.exists("env.py"):
    import env

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', '')

# DEBUG = 'DEVELOPMENT' in os.environ
DEBUG = (
    os.environ.get('DEBUG', 'False') == 'True' or 'DEVELOPMENT' in os.environ
)

ALLOWED_HOSTS = [
    '127.0.0.1',
    '8000-cptvalleybe-tempusautho-9ix7ubfd2ya.ws.codeinstitute-ide.net',
    '.herokuapp.com',
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.codeinstitute-ide.net/",
    "https://*.herokuapp.com"
]

# Application definition
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'csp',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.sites',
    'home',
    'works',
    'checkout',
    'profiles',
    'about',
    'blog',

    # Other apps
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'django_summernote',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'tempusap_config.urls'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    'GET',
    'OPTIONS'
]

CORS_ALLOW_CREDENTIALS = True

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'works.context_processors.bookcart_contents',
                'tempusap_config.context_processors.google_form_url',
            ],
        },
    },
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Email settings
DEFAULT_FROM_EMAIL = '"Tempus Author Platform" <tempus@valleyberg.com>'
CONTACT_DISPLAY_EMAIL = 'tempus@valleyberg.com'
CONTACT_DISPLAY_NAME = 'Tempus Author Platform'

if 'DEVELOPMENT' in os.environ:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.dreamhost.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

    EMAIL_TIMEOUT = 3
    EMAIL_USE_SSL = False

# Allauth settings
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

WSGI_APPLICATION = 'tempusap_config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AWS S3 settings
USE_AWS = os.environ.get('USE_AWS') == 'True'

if USE_AWS:
    # Bucket Config - Very Important!
    AWS_STORAGE_BUCKET_NAME = 'tempusap-bucket'
    AWS_S3_REGION_NAME = 'eu-north-1'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = (
        f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
    )

    # S3 Settings - Super Important!
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_FILE_OVERWRITE = False
    AWS_QUERYSTRING_AUTH = False

    # Tell Django to use S3 for storage
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": "media"
            }
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": "static"
            }
        }
    }

    # Override static and media URLs in production
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:
    # Use local storage for static and media files in development
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage"
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }

# Content Security Policy
CSP_DEFAULT_SRC = [
    "'self'",
    "https://script.google.com",
    "https://*.google.com",
    "https://*.googleusercontent.com",
    "*.amazonaws.com"
]
CSP_STYLE_SRC = [
    "'self'",
    "'unsafe-inline'",
    "*.amazonaws.com",
    "*.googleapis.com",
    "*.cdnjs.cloudflare.com",
    "*.jsdelivr.net",
    "*.bootstrapcdn.com",
    "stackpath.bootstrapcdn.com",
    "https://*.jsdelivr.net",
    "https://*.amazonaws.com",
    "https://*.googleapis.com",
    "https://*.cdnjs.cloudflare.com",
    "https://*.jsdelivr.net",
    "https://*.bootstrapcdn.com",
]
CSP_STYLE_SRC_ELEM = [
    "'self'",
    "'unsafe-inline'",
    "*.amazonaws.com",
    "*.googleapis.com",
    "*.cdnjs.cloudflare.com",
    "*.jsdelivr.net",
    "*.bootstrapcdn.com",
    "stackpath.bootstrapcdn.com",
    "https://*.amazonaws.com",
    "https://*.googleapis.com",
    "https://*.cdnjs.cloudflare.com",
    "https://*.jsdelivr.net",
    "https://cdnjs.cloudflare.com",
    "https://*.bootstrapcdn.com",
    "cdnjs.cloudflare.com"
]
CSP_SCRIPT_SRC = [
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "*.amazonaws.com",
    "*.jquery.com",
    "*.jsdelivr.net",
    "*.stripe.com",
    "*.bootstrapcdn.com",
    "stackpath.bootstrapcdn.com",
]
CSP_IMG_SRC = [
    "'self'",
    "*.amazonaws.com",
    "https://*.amazonaws.com",
    "data:",
    "blob:",
]
CSP_FONT_SRC = [
    "'self'",
    "*.googleapis.com",
    "*.gstatic.com",
    "*.cdnjs.cloudflare.com",
    "*.amazonaws.com",
    "*.bootstrapcdn.com",
    "stackpath.bootstrapcdn.com",
    "https://*.googleapis.com",
    "https://*.gstatic.com",
    "https://*.cdnjs.cloudflare.com",
    "https://cdnjs.cloudflare.com",
    "https://*.amazonaws.com",
    "https://*.bootstrapcdn.com",
    "http://*.bootstrapcdn.com",
    "cdnjs.cloudflare.com",
    "data:",
]
CSP_CONNECT_SRC = [
    "'self'",
    "*.stripe.com",
    "https://script.google.com",
    "https://*.google.com",
    "https://*.googleusercontent.com",
]
CSP_FRAME_SRC = [
    "'self'",
    "*.stripe.com",
    "https://script.google.com",
    "https://*.google.com",
    "https://*.googleusercontent.com",
]
CSP_INCLUDE_NONCE_IN = ['script-src']

# Google Apps Script URL for newsletter signup
GOOGLE_FORM_URL = os.environ.get('GOOGLE_FORM_URL')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database Configuration
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Stripe settings
STRIPE_CURRENCY = 'usd'
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')

# Summernote settings
SUMMERNOTE_CONFIG = {
    'attachment_filesize_limit': 5 * 1024 * 1024,  # 5MB limit
}

# Profile Image upload settings
MAX_UPLOAD_SIZE = 2 * 1024 * 1024  # 2MB lmit
MAX_IMAGE_WIDTH = 1800
MAX_IMAGE_HEIGHT = 1800
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']
