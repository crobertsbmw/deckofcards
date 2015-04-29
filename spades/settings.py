# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

DEBUG = True


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!-cbgozl)5ybco&c%&iub1j%+tps9nhpz!1jw4kr+kdd!f5f!@'


ALLOWED_HOSTS = ['.spades.com']

AUTH_USER_MODEL = 'deck.User'

EMAIL_USE_TLS = True
EMAIL_HOST = 'in-v3.mailjet.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'b411d13c81b708040dd4c15a6fa1c9df'
EMAIL_HOST_PASSWORD = 'ed2fe46b4984bd1fba35ecebf4aca2f4'

STATICFILES_DIRS = (
    '/Users/croberts/spades/static/',
)
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'deck',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'spades.urls'

WSGI_APPLICATION = 'spades.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'MST'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = BASE_DIR+'/media/'
MEDIA_URL = '/media/'