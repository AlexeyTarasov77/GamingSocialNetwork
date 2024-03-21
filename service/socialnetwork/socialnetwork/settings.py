"""
Django settings for socialnetwork project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  
]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = ['127.0.0.1', '0.0.0.0', 'localhost', '192.168.65.1']

# Application definition

DJANGO_APPS = [
    'daphne', # run django on asgi server
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.postgres'
]

THIRD_PARTY_APPS = [
    'taggit',
    'rest_framework',
    'mptt',
    "allauth_ui",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.openid',
    'allauth.socialaccount.providers.discord',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.steam',
    'widget_tweaks',
    'channels',
    'django_celery_results',
    'django_celery_beat',
    'sorl.thumbnail',
    'debug_toolbar',
]

LOCAL_APPS = [
    'users.apps.UsersConfig',
    'articles.apps.ArticlesConfig',
    'chat.apps.ChatConfig',
    'events.apps.EventsConfig',
    'gameblog.apps.GameblogConfig',
    'posts.apps.PostsConfig',
    'searchteam.apps.SearchteamConfig',
    'cart.apps.CartConfig',
    'gameshop.apps.GameshopConfig',
    'actions.apps.ActionsConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'socialnetwork.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'gameblog.context_processors.menu_links',
                'gameblog.context_processors.sidebar_links',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'socialnetwork.wsgi.application'
ASGI_APPLICATION = 'socialnetwork.asgi.application' 

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'), 
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# cache configuration

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/1",
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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


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

# USE INSENSITIVE TAGS
TAGGIT_CASE_INSENSITIVE = True

#MEDIA FILES CONFIG
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# EMAIL SMTP SERVER CONFIG
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# REST FRAMEWORK

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# ALL_AUTH

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_CHANGE_EMAIL = True # разрешить пользователю изменять email
ACCOUNT_EMAIL_REQUIRED = True # обязательное указание емаила при реге
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True # залогинить юзера при потдтверждении емеила
LOGIN_URL = 'account_login' # имя маршрута для редиректа неавторизованных юзеров
LOGIN_REDIRECT_URL = "users:profile_middleware" # редирект после успешного логина
LOGOUT_REDIRECT_URL = 'account_login' # редирект после логаута
ACCOUNT_PRESERVE_USERNAME_CASING = False # хранить юзернеймы в нижнем регистре
ACCOUNT_USERNAME_MIN_LENGTH = 3

# CELERY 

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/2'
CELERY_CACHE_BACKEND = 'default'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# REDIS FOR APPS

REDIS_HOST = 'redis'
REDIS_PORT = '6379'
REDIS_DB = 3

# CART SESSION KEY

CART_SESSION_KEY = 'cart'