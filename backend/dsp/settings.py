import os
from decouple import config
from pathlib import Path
from datetime import timedelta
import boto3
from botocore.client import Config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="unsafe-secret-key")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = ['abhiaryz.pythonanywhere.com','pythonanywhere.com' ,'.now.sh', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "social_django",
    "api",
    'drf_yasg',
    'storages',
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dsp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Add this line if not present
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dsp.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "dsp.urls"
# S3 Static and Media Settings
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "<YOUR_GOOGLE_CLIENT_ID>"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "<YOUR_GOOGLE_CLIENT_SECRET>"

# Configure redirects
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/authenticated/"
SOCIAL_AUTH_LOGIN_ERROR_URL = "/login-error/"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '<your-email>@gmail.com'
EMAIL_HOST_PASSWORD = '<your-email-password>'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://ad-campaign.vercel.app/",
]

CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

AWS_ACCESS_KEY_ID="AKIA4MTWN4X3A6OBKQNH"
AWS_SECRET_ACCESS_KEY="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"
AWS_STORAGE_BUCKET_NAME="test-mmr-dsp"
AWS_S3_REGION_NAME="ap-south-1"
AWS_S3_CUSTOM_DOMAIN="test-mmr-dsp.s3.amazonaws.com"
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False  # Optional: make files public

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

s3 = boto3.resource(
    "s3",
    region_name=AWS_S3_REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=Config(signature_version="s3v4"),
)

BUCKET = s3.Bucket(AWS_STORAGE_BUCKET_NAME)

AWS_LOCATION = "static"
AWS_DEFAULT_ACL = None

STATIC_URL = "https://test-mmr-dsp.s3.amazonaws.com/static/"
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/"

INSTALLED_APPS += ['rest_framework_simplejwt.token_blacklist']

AWS_QUERYSTRING_AUTH = True