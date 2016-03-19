# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ttek+!i(88ig4a9ca*c-ehct@6a!jyqn()5e675!@ya5o*0_wf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

MANTENIMIENTO = False

ALLOWED_HOSTS = [ '*' ]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    'rest_framework',
    'unidaddiagnosticomolecular',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',                       
)

AUTH_USER_MODEL = 'unidaddiagnosticomolecular.UDMUser'

ROOT_URLCONF = 'unidaddiagnosticomolecular.urls'

WSGI_APPLICATION = 'unidaddiagnosticomolecular.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-VE'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

APLICACION = 'unidaddiagnosticomolecular'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'postgres',                                  # Or path to database file if using sqlite3.
        'USER': 'postgres',                                  # Not used with sqlite3.
        'PASSWORD': 'manager1',                              # Not used with sqlite3.
        'HOST': 'localhost',                                 # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
            'options': '-c search_path=udmtest'                  # Set the schema
        },
        'ATOMIC_REQUESTS': True,		
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler', 
            'filename': '/var/logs/udmtest/unidaddiagnosticomolecular.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount':10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': [ 'console', 'file' ],
            'level': 'ERROR',
            'propagate': False,
        },
        'commons.convit': {
            'handlers': [ 'console', 'file' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'unidaddiagnosticomolecular': {
            'handlers': [ 'console', 'file' ],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s|%(levelname)s|%(message)s'
        }
    },
}

TEMPLATE_DIRS = (    
  os.path.join(BASE_DIR, 'templates').replace('\\','/'),
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'html/static/'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'html/static')

URL_PREFIX = '/udmtest'
STATIC_URL = URL_PREFIX + '/static/'
LOGIN_URL = URL_PREFIX + '/login'
LOGIN_REDIRECT_URL = URL_PREFIX + '/'

EMAIL_SERVER_USERNAME = 'diagnostico.molecular@jacintoconvit.org'
EMAIL_SERVER_PASSWORD = 'cad877723spd23@D55x'
EMAIL_SERVER_URL = 'smtp.gmail.com:587'
