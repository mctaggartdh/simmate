"""
Django settings for project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from simmate import website  # needed to specify location of apps
from simmate import database  # needed to specify database location

# The base directory is where simmate.website is located
BASE_DIR = os.path.dirname(os.path.abspath(website.__file__))

# The database directory is where simmate.database is located. I move the
# default database file into the simmate.database module.
# TODO: consider placing the database in the user's .simmate/ configuration
# directory so they can easily share/delete it.
DATABASE_DIR = os.path.dirname(os.path.abspath(database.__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "ts@sqlo4ky*4*^*+iezl%^-^i^yfbqir#ref5_or4@x8i49(o$"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

# !!! I can add "simmate.website." if I'm not using django within a package
INSTALLED_APPS = [
    "simmate.website.accounts.apps.AccountsConfig",
    "simmate.website.diffusion.apps.DiffusionConfig",
    "simmate.website.execution.apps.ExecutionConfig",
    "crispy_forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
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

# "core" here is based on the name of my main django folder
ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # I set DIRS below so I can have a single templates folder
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

# "core" here is based on the name of my main django folder
WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# BUG: django docs say to always use forward slashes, but it works just fine
# without them... For now, I don't inlcude the .replace("\\", "/").
DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": os.path.join(DATABASE_DIR, "db.sqlite3"),
    # }
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "simmate-test-pool",  # default on DigitalOcean is defaultdb
        "USER": "doadmin",
        "PASSWORD": "dibi5n3varep5ad8",
        "HOST": "db-postgresql-nyc3-09114-do-user-8843535-0.b.db.ondigitalocean.com",
        "PORT": "25061",
    }
}

# $ dropdb development_db_name
# $ createdb developmnent_db_name

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth."
            "password_validation.UserAttributeSimilarityValidator"
        ),  # formatted in this odd way because of line length limit for Black
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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

DATETIME_INPUT_FORMATS = [
    "%Y-%m-%dT%H:%M",  # this is a custom format I added to get my form widgets working.
    "%Y-%m-%d %H:%M:%S",  # '2006-10-25 14:30:59'
    "%Y-%m-%d %H:%M:%S.%f",  # '2006-10-25 14:30:59.000200'
    "%Y-%m-%d %H:%M",  # '2006-10-25 14:30'
    "%Y-%m-%d",  # '2006-10-25'
    "%m/%d/%Y %H:%M:%S",  # '10/25/2006 14:30:59'
    "%m/%d/%Y %H:%M:%S.%f",  # '10/25/2006 14:30:59.000200'
    "%m/%d/%Y %H:%M",  # '10/25/2006 14:30'
    "%m/%d/%Y",  # '10/25/2006'
    "%m/%d/%y %H:%M:%S",  # '10/25/06 14:30:59'
    "%m/%d/%y %H:%M:%S.%f",  # '10/25/06 14:30:59.000200'
    "%m/%d/%y %H:%M",  # '10/25/06 14:30'
    "%m/%d/%y",  # '10/25/06'
]

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
# !!! Consider removing in the future.
USE_I18N = True

# !!! I changed this setting to get my datetime-local widgets working, but I don't
# !!! understand active locals -- I need to read more
# !!! https://docs.djangoproject.com/en/3.0/ref/forms/fields/#datetimefield
USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# collect by running 'python manage.py collectstatic'
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# This sets the django-crispy formating style
CRISPY_TEMPLATE_PACK = "bootstrap4"

# options for login/logoff
# LOGIN_REDIRECT_URL = "/accounts/profile/"  # this is the default
LOGOUT_REDIRECT_URL = "/accounts/loginstatus/"

# Settings for sending emails with my gmail account
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # this is the default
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "jacksundberg123@gmail.com"  # os.environ.get('EMAIL_USER')
# !!! REMOVE IN PRODUCTION. Use this instead: os.environ.get('EMAIL_PASSWORD')
EMAIL_HOST_PASSWORD = "lqurjxyttrjrlgcr"