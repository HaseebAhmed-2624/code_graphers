import os
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers
from corsheaders.defaults import default_methods

from .. import env

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('SECRET_KEY', '*************')

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Application definition


INSTALLED_APPS = [
    # builtin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # packages
    'drf_yasg',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    "corsheaders",
    'anymail',
    'django.contrib.admindocs',

]

if env.bool("USE_DJANGO_EXTENSIONS", False):
    INSTALLED_APPS.append('django_extensions')

PROJECT_APPS = [
    'apps.auth_.apps.AuthConfig',
    'apps.trades.apps.TradesConfig',
    'apps.utils.apps.UtilsConfig',
]

INSTALLED_APPS += PROJECT_APPS
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

ASGI_APPLICATION = "config.asgi.application"

# Password validation
if env.bool("USE_PASSWORD_VALIDATORS", True):
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
        {
            'NAME': 'apps.utils.helpers.validators.HasUpperCaseLetter',
        },
        {
            'NAME': 'apps.utils.helpers.validators.HasSpecialCharacter',
        },
        {
            'NAME': 'apps.utils.helpers.validators.HasNumericDigit',
        },
    ]
else:
    AUTH_PASSWORD_VALIDATORS = []
# Internationalization


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Setting UserModel
AUTH_USER_MODEL = "auth_.User"

# File Manger
MAX_FILE_UPLOAD_SIZE = env.int("MAX_FILE_UPLOAD_SIZE", 1024 * 1024 * 1024 * 2)

# Global Variables
API_VERSION = env.int("API_VERSION", 1)

REST_FRAMEWORK = {

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.utils.auth.CustomJWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'apps.utils.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/day',
        'user': '1000/day'
    },
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "EXCEPTION_HANDLER": "apps.utils.exceptions.handler.custom_exception_handler",
    "NON_FIELD_ERRORS_KEY": "message",
}

# _______SIMPLEJWT_SETTINGS_______

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(weeks=50),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
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

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# ________EMAIL_CONFIGURATION________
FORGOT_PASSWORD_EMAIL_REDIRECT_URL = env.str("FORGOT_PASSWORD_EMAIL_REDIRECT_URL")
EMAIL_VERIFICATION_TIMEOUT_SECONDS = env.int("EMAIL_VERIFICATION_TIMEOUT_SECONDS")

SERVER_URL = os.getenv('SERVER_URL', 'http://127.0.0.1:8000')

# _________CORS_CONFIGURATION_____________
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_METHODS = (*default_methods,)
CORS_ALLOW_HEADERS = (*default_headers,)
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS")

print("DEBUG_MODE", DEBUG, "\n", "allowed origins", CORS_ALLOWED_ORIGINS, "\n", "trusted origins", CSRF_TRUSTED_ORIGINS)
# __________CELERY_QUEUES_____________

CELERY_TASK_DEFAULT_QUEUE = 'DEFAULT_Q'

CELERY_TASK_QUEUES = {
    'low_priority': {
        'exchange': 'LOW_PRIORITY_Q',
        'routing_key': 'LOW_PRIORITY_Q',
    },
    'high_priority': {
        'exchange': 'HIGH_PRIORITY_Q',
        'routing_key': 'HIGH_PRIORITY_Q',
    },
    'default': {
        'exchange': 'DEFAULT_Q',
        'routing_key': 'DEFAULT_Q',
    },
}
CELERY_TIMEZONE = env.str("CELERY_TIMEZONE", "UTC")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = env.str("CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP", True)
CELERY_CACHE_BACKEND = 'default'
CELERY_WORKER_REVOKES_MAX = env.int("CELERY_WORKER_REVOKES_MAX", 1000)

# ___________WEBSOCKETS__________
WEBSOCKET_TIMEOUT_SECONDS = env.int('WEBSOCKET_TIMEOUT_SECONDS', 25)
CRYPTO_AES_KEY = env.str("CRYPTO_AES_KEY", "****************")

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "mediafiles")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "staticfiles")
STATIC_URL = "/static/"

# __________EMAIL_SETUP_________
EMAIL_HOST = env('EMAIL_HOST', default='**********')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER')  # Your sender email username
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = env.str("SERVER_EMAIL")
ADMIN_EMAIL = env.str("ADMIN_EMAIL")
EMAIL_USE_TLS = True

# __________BREVO_SETUP_________
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
ANYMAIL_BREVO_API_KEY = env.str("BREVO_API_KEY")

USE_PROD_DATABASE = env.bool('USE_PROD_DATABASE', False)
DEV_MODE = env.bool('DEV_MODE', False)
# ________DATABASE__________
if env.str("DJANGO_SETTINGS_MODULE") == 'config.settings.production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env.str("POSTGRES_DB"),
            'USER': env.str("POSTGRES_USER"),
            'PASSWORD': env.str("POSTGRES_PASSWORD"),
            'HOST': env.str("POSTGRES_HOST"),
            'PORT': env.str("POSTGRES_PORT", 5432),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")

# ________REDIS_CONFIGURATION________
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CELERY_BROKER_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": CELERY_BROKER_URL},
    },
}
# ________LOGGER___________
if env.bool('USE_DJANGO_LOGGER', False):
    LOGGING = {
        'version': 1,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['console'],
            }
        }
    }

# _________STRIPE___________________
STRIPE_API_KEY = env.str("STRIPE_API_KEY", "********")
STRIPE_PUBLISHABLE_KEY = env.str("STRIPE_PUBLISHABLE_KEY", "********")
STRIPE_WEBHOOK_SECRET = env.str("STRIPE_WEBHOOK_SECRET", "*********")

ANY_API_KEY = env.str("ANY_API_KEY")
FRONTEND_URL = env.str("FRONTEND_URL")
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
