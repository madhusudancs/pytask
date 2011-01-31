# Django settings for pytask project.

import os

from pytask.local import *


ADMINS = (
    ('Madhusudan C.S.', 'madhusudancs@fossee.in'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/pytask/media/'

# Absolute path to the directory that holds static files.
# Example: "/home/static-files/static-files.lawrence.com/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

# URL that handles the static files served from STATIC_ROOT. Make sure to use
# a trailing slash if there is a path component (optional in other cases).
# Examples: "http://static-files.lawrence.com",
# "http://example.com/static-files/"
STATIC_URL = '/pytask/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/pytask/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^ww=xk&idt)=03kqg*fz8x%=dqbhh1kd2z=f%$m@r9_+9b=&x='

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'pytask.taskapp.context_processors.configuration',
    )

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pytask.middleware.exceptions.ExceptionMiddleware',
)

ROOT_URLCONF = 'pytask.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django_extensions',
    'registration',
    'tagging',
    'south',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'pytask',
    'pytask.profile',
    'pytask.taskapp',
)

AUTH_PROFILE_MODULE = 'profile.Profile'

#django-registration
ACCOUNT_ACTIVATION_DAYS = 7
DEFAULT_FROM_EMAIL = 'FOSSEE Admin <admin@fossee.in>'
