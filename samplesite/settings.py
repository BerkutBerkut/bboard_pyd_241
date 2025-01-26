"""
Django settings for samplesite project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

from captcha.conf.settings import CAPTCHA_TIMEOUT, CAPTCHA_LENGTH
from django.conf.global_settings import STATICFILES_DIRS, ABSOLUTE_URL_OVERRIDES, MEDIA_URL, AUTH_USER_MODEL
from django_bootstrap5.core import BOOTSTRAP5

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-oec=ed+f%7&937eu**k-z9c)5n)qap@7u#a8%+5&jwo@wuvy8#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 'django.contrib.postgres',
    "captcha",
    "precise_bbcode",
    "django_bootstrap5",
    "easy_thumbnails",
    "bboard",  # 'bboard.apps.BboardConfig',
    "testapp",
    "todolist",
    "django_cleanup",  # всегда в самом низу!!!
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'samplesite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'samplesite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 'ATOMIC_REQUEST': True, # False,
        # 'AUTOCOMMIT': False, # True,
    }
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql_psycopg2",
    #     "NAME": "django_db",
    #     "USER": "db_user",
    #     "PASSWORD": "12345",
    #     "HOST": "127.0.0.1",
    #     "PORT": "5433",
    # }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
    # {
    #     "NAME": "bboard.validators.NoForbiddenCharsValidator",
    #     "OPTIONS": {"forbidden_chars": (" ", ",", ".", ":", ";")},
    # },
    # {
    #     "NAME": "bboard.validators.CustomPasswordValidator",
    # },
]

# AUTH_USER_MODEL = 'testapp.models.AdvUser'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
# STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ABSOLUTE_URL_OVERRIDES = {
#     'bboard.rubric': lambda rec: f"{rec.pk}/"
# }

DEFAULT_CHARSET = 'utf-8'

# Логирование данных запроса в текстовый файл
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'request_logs.txt',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

LOGIN_URL = "/login/" # URL для входа
LOGIN_REDIRECT_URL = "bboard:index"  # URL после выхода
LOGOUT_REDIRECT_URL = "bboard:index"  # URL после входа
# PASSWORD_RESET_TIMEOUT = 60 * 60 * 24 * 3  # 259_200

# CAPTCHA
# CAPTCHA_CHALLENGE_FUNCT ='captcha.helpers.random_char_challenge',
# CAPTCHA_CHALLENGE_FUNCT ='captcha.helpers.math_challenge',
# CAPTCHA_CHALLENGE_FUNCT ='captcha.helpers.word_challenge'

# CAPTCHA_TIMEOUT = 5 # minutes
CAPTCHA_LENGTH = 4 # 4 ПО УМОЛЧАНИЮ

# CAPTCHA_WORDS_DICTIONARY = BASE_DIR / 'static/bboard/words.txt'

# CAPTCHA_LETTER_ROTATION = (-95, -95)


# DATA_UPLOAD_MAX_MEMORY_SIZE = 2_621_440 # по умолчанию 2.5 Mb
# DATA_UPLOAD_MAX_NUMBER_FIELD = 1000

# BBCODE
# BBCODE_NEWLINE = '<br>'
# BBCODE_ALLOW_CUSTOM_TAGS = False

BOOTSTRAP5 = {
    "required_css_class": "required",
    "success_css_class": "has-success",
    "error_css_class": "has-error",
}

# настройка easy-thumbnails
THUMBNAIL_ALIASES = {
    "bboard.Bb.img": {
        "default": {
            "size": (500, 300),
            "crop": "scale",
        },
    },
    "testapp": {
        "default": {
            "size": (400, 300),
            "crop": "smart",
            "bw": True,
        },
    },
    "": {
        "default": {
            "size": (180, 240),
            'crop': 'scale',
        },
        "big": {
            'size': (480, 640),
            'crop': '10,10'
        },
    },
}

THUMBNAIL_DEFAULT_OPTIONS = {
    'quality': 90,
    'subsampling': 1,
}

# THUMBNAIL_MEDIA_URL = "/media/thumbnail/"
# THUMBNAIL_MEDIA_ROOT = BASE_DIR / "media/thumbnail/"
THUMBNAIL_SUBDIR = 'thumbs'
# THUMBNAIL_PREFIX = "thumbs"
# THUMBNAIL_EXTENSION = 'jpg'
# THUMBNAIL_TRANSPARENCY_EXTENSION = 'png'
THUMBNAIL_PRESERVE_EXTENSION = ('png',)
