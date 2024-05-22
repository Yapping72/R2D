from pathlib import Path
import os
from datetime import timedelta
import subprocess

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist', # for black listing of refresh tokens
    'framework', # contains the framework and base classes to be used throughout the project
    'accounts', # contains custom user class
    'authentication', # contains simplejwt authentication & authorization components
    'notification', # contains notification 
    'application_logging', # application logging 
    'admin_portal', # contains admin portal
]

# White listing the localhost:5143 for React Frontend
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", 
    "https://localhost",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'django_backend_r2d.urls'

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

WSGI_APPLICATION = 'django_backend_r2d.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Prevent Browsable API
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),

    # Throttling rates
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour', # anonymous users can make up to 100 request per hour
        'user': '1000/hour', # authenticated users can make up to 1000 request per hour
    }
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"), 
        "USER": os.getenv("POSTGRES_USER"),  
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),  
        "HOST": "postgres_r2d_db",  
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10), 
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1), # refresh token allows user to be logged in for 1 days before needing to login again
    "ROTATE_REFRESH_TOKENS": True, # if user has used website within 1days new refresh token wil be automatically generated without the need to login
    "BLACKLIST_AFTER_ROTATION": True, # to prevent reusing of refresh tokens set to true i.e., only most recent token is used
    "UPDATE_LAST_LOGIN": True, # updates user model whenever a token is obtained

    "ALGORITHM": "RS256",
    "AUDIENCE": "React-Frontend-R2D",
    "ISSUER": "Django-Backend-R2D",
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",
    "TOKEN_OBTAIN_SERIALIZER": "authentication.services.serializers.CustomTokenPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
}

# Paths for the private and public keys
signing_key = os.path.join("secrets", "private_key.pem")
verifying_key = os.path.join("secrets", "public_key.pem")

# Check if the private key file exists
if not os.path.exists(signing_key):
    # The private key file does not exist, so create it
    try:
        subprocess.run(['openssl', 'genpkey', '-algorithm', 'RSA', '-out', signing_key], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating private key: {e}")
    else:
        print(f"Private key generated at {signing_key}")

# Check if the public key file exists
if not os.path.exists(verifying_key):
    # The public key file does not exist, so create it
    try:
        subprocess.run(['openssl', 'rsa', '-pubout', '-in', signing_key, '-out', verifying_key], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating public key: {e}")
    else:
        print(f"Public key generated at {verifying_key}")

try: 
    with open(signing_key, 'r') as f:
        SIMPLE_JWT['SIGNING_KEY'] = f.read()
except FileNotFoundError:
    print(f"Failed to find {signing_key}")

try:
    with open(verifying_key, 'r') as f:
        SIMPLE_JWT['VERIFYING_KEY'] = f.read()
except FileNotFoundError:
    print(f"Failed to find {verifying_key}")
