"""
Django settings for igconnect project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#q6b(iam%6w1205l61^%*1nd!#))amalx=qc9d2(4dg&obj-p9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auth',
    'dashboard',
    'djangotoolbox',
    'profileSpace',
    'searchig',
    'event',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'igconnect.urls'

WSGI_APPLICATION = 'igconnect.wsgi.application'

# Database Settings

USERNAME_DB = 'priyam' #username for your database
PASSWORD_DB = 'priyam123' #password for your database
DATABASES = {
    'default': {
    'ENGINE': 'django_mongodb_engine',
    'NAME': 'igconnect_db',
    'USER':USERNAME_DB,
    'PASSWORD':PASSWORD_DB,
    'HOST' : '127.0.0.1',
    'PORT' : '',

    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


TEMPLATE_DIRS = ('./templates',)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
AUTH_PROFILE_MODULE = 'auth.UserProfile'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
