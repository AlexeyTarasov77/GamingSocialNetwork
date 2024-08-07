"""
Django settings for socialnetwork project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = ["127.0.0.1", "0.0.0.0", "localhost", "192.168.65.1"]

# Application definition

DJANGO_APPS = [
    "daphne",  # run django on asgi server
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.postgres",
]

THIRD_PARTY_APPS = [
    "taggit",
    "rest_framework",
    "rest_framework_simplejwt",
    "mptt",
    "allauth_ui",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.openid",
    "allauth.socialaccount.providers.discord",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.steam",
    "widget_tweaks",
    "crispy_forms",
    "crispy_bootstrap5",
    "channels",
    "django_celery_results",
    "django_celery_beat",
    "django_countries",
    "sorl.thumbnail",
    "debug_toolbar",
    "algoliasearch_django",
    "rosetta",
]

LOCAL_APPS = [
    "users.apps.UsersConfig",
    "chats.apps.ChatsConfig",
    "events.apps.EventsConfig",
    "gameblog.apps.GameblogConfig",
    "posts.apps.PostsConfig",
    "gameteams.apps.GameteamsConfig",
    "cart.apps.CartConfig",
    "gameshop.apps.GameshopConfig",
    "actions.apps.ActionsConfig",
    "orders.apps.OrdersConfig",
    "payment.apps.PaymentConfig",
    "coupons.apps.CouponsConfig",
    "api.apps.ApiConfig",
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

LOG_SQL = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname}|{asctime}|{module}:{lineno}|{name}>> {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file_general": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "general_log.log"),
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file_general"],
        "level": "ERROR",
    },
    "loggers": {
        # "django": {
        #     "handlers": ["console", "file"],
        #     "level": "INFO",
        #     "propagate": True,
        # },
        # "gameblog": {
        #     "handlers": ["console", "file"],
        #     "level": "INFO",
        #     "propagate": True,
        # },
    },
}


def create_app_loger(app_name):
    app_name = app_name.split(".")[0]  # remove .apps.AppConfig
    if app_name not in LOGGING["loggers"]:
        app_handler = {
            **LOGGING["handlers"]["file_general"],
            "filename": os.path.join(BASE_DIR, ".logs", f"{app_name}_log.log"),
        }
        LOGGING["handlers"][app_name + "_handler"] = app_handler
        LOGGING["loggers"][app_name] = {
            "handlers": [app_name + "_handler"],
            "level": "DEBUG",
            "propagate": False,
        }


for app_name in LOCAL_APPS:
    create_app_loger(app_name)

if LOG_SQL:
    LOGGING["loggers"]["django.db.backends"] = {
        "handlers": ["console"],
        "level": "DEBUG",
    }


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "socialnetwork.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "gameblog.context_processors.menu_links",
                "gameblog.context_processors.sidebar_links",
                "gameblog.context_processors.indices",
                "cart.context_processors.cart",
            ],
        },
    },
]

WSGI_APPLICATION = "socialnetwork.wsgi.application"
ASGI_APPLICATION = "socialnetwork.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# cache configuration

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "memcached:11211",
    }
}

CACHE_KEY_PREFIX = "socialnetwork"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGES = [
    ("en", _("English")),
    ("ukr", _("Ukrainian")),
    ("ru", _("Russian")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


#    <-----CUSTOM SETTINGS------>

# DJANGO-CHANNELS
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

# CRISPY FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# USE INSENSITIVE TAGS
TAGGIT_CASE_INSENSITIVE = True

# MEDIA FILES CONFIG
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
DEFAULT_IMAGE_URL = os.path.join(MEDIA_URL, "photos/default.jpeg")

# EMAIL SMTP SERVER CONFIG
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# REST FRAMEWORK

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

# ALL_AUTH

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_CHANGE_EMAIL = True  # разрешить пользователю изменять email
ACCOUNT_EMAIL_REQUIRED = True  # обязательное указание емаила при реге
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True  # залогинить юзера при потдтверждении емеила
LOGIN_URL = "account_login"  # имя маршрута для редиректа неавторизованных юзеров
LOGIN_REDIRECT_URL = "users:profile_middleware"  # редирект после успешного логина
LOGOUT_REDIRECT_URL = "account_login"  # редирект после логаута
ACCOUNT_PRESERVE_USERNAME_CASING = False  # хранить юзернеймы в нижнем регистре
ACCOUNT_USERNAME_MIN_LENGTH = 3

# CELERY

CELERY_BROKER_URL = "amqp://guest:guest@rabbitmq:5672//"
CELERY_RESULT_BACKEND = "redis://redis:6379/2"
CELERY_CACHE_BACKEND = "default"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# REDIS FOR APPS

REDIS_HOST = "redis"
REDIS_PORT = "6379"
REDIS_DB = 3

# CART SESSION KEY

CART_SESSION_KEY = "cart"

# STRIPE SETTINS

STRIPE_PUBLISH_KEY = os.getenv("STRIPE_PUBLISH_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_API_VERSION = "2023-10-16"
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# ALGOLIA SEARCH ENGINE

ALGOLIA = {
    "APPLICATION_ID": os.getenv("ALGOLIA_APPLICATION_ID"),
    "API_KEY": os.getenv("ALGOLIA_API_KEY"),
}
