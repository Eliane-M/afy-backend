from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv
from firebase_admin import credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PRODUCTION = True
BASE_DIR = Path(__file__).resolve().parent.parent


# Load the .env file
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
SERVER_API_TOKEN = os.getenv("SERVER_API_TOKEN")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "agriculture-for-youth-o50f.onrender.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'agri',
    'authentication',
    'base',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://agriculture-for-youth-o50f.onrender.com",
]

CORS_ALLOW_HEADERS = [
    'content-type',
    'x-requested-with',
    'authorization',
    'accept',
    'accept-encoding',
    'origin',
    'user-agent',
    'dont',
    'cache-control',
    'x-csrftoken',
    'x-requested-with',
    'x-xsrftoken',
]

CORS_ALLOW_METHODS = [
    'GET', 
    'POST', 
    'PUT', 
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USERNAME"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("TEST_DB_NAME"),
            "USER": os.getenv("TEST_DB_USERNAME"),
            "PASSWORD": os.getenv("TEST_DB_PASSWORD"),
            "HOST": os.getenv("TEST_DB_HOST"),
            "PORT": os.getenv("TEST_DB_PORT"),
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

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]

from core.firebase_bucket_credentials import firebase_credentials
import firebase_admin

credential=firebase_credentials()


cred = credentials.Certificate(credential)
firebase_admin.initialize_app(cred, options={"storageBucket": credential["storageBucket"]})


DEFAULT_FILE_STORAGE = 'core.firebase.FirebaseStorage' 

if not DEBUG:   

    #Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    # Turn on WhiteNoise storage backend that takes   care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'core.firebase.FirebaseStorage'

else:
    MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}


REST_FRAME_SIMPLEJWT = {
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.RefreshToken",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
     'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

#emails

EMAIL_BACKEND = "postmark.django_backend.EmailBackend"
DEFAULT_FROM_EMAIL = os.getenv("MAIN_EMAIL")
EMAIL_SERVER_TOKEN = os.getenv("EMAIL_SERVER_TOKEN")
POSTMARK_API_KEY = os.getenv("POSTMARK_API_KEY")