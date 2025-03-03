from django.conf.global_settings import STATICFILES_DIRS, MEDIA_ROOT, MEDIA_URL
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

IN_DOCKER = os.getenv('DOCKER_CONTAINER', False)
IN_PRODUCTION = os.getenv('IN_PRODUCTION', False)

DEBUG = IN_PRODUCTION

if not IN_PRODUCTION:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['data-training-production.up.railway.app']
    CSRF_TRUSTED_ORIGINS = ['https://data-training-production.up.railway.app']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
    'bootstrap5',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'DataTraining.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates",
                 BASE_DIR / "dashboard/templates/dashboard/components",],
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

WSGI_APPLICATION = 'DataTraining.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if IN_PRODUCTION or IN_DOCKER:

    DATABASES = {
        'default': {

            'ENGINE': 'django.db.backends.postgresql_psycopg2',

            'NAME': "data-training",

            'USER': "avnadmin",

            'PASSWORD': os.getenv('PASSWORD'),

            'HOST': os.getenv('HOST'),

            'PORT': os.getenv('PORT'),

        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'data_training',
            'USER': 'postgres',
            'PASSWORD': os.getenv('POSTGRES_DB_PASS'),
            'HOST': '127.0.0.1',
            'PORT': '5432',

        }
    }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.mysql',
#          'NAME': 'defaultdb',
#          'USER': 'avnadmin',
#          'PASSWORD': os.getenv('MYSQL_PASSWORD'),
#          'HOST': os.getenv('MYSQL_HOST'),
#          'PORT': os.getenv('MYSQL_PORT'),
#      }
#  }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'




MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if IN_PRODUCTION:
    CELERY_BROKER_URL = os.getenv('REDIS_URL')
else:
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True