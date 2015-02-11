"""
Django settings for wsd_games project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import json
with open(os.path.dirname(__file__) + "/../client_secrets.json", "r") as jsonf:
    client_secrets = json.load(jsonf)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'si66cc5d0bpf6#kzte6f$*z@()(m@hcery*_n$ie=h(8y*6vr*'

# SID and secret key for payment service, keep these secret!
SID = "WsdGamesCo"
SID_KEY = "5dd2d7e5adfb3cfb061e4f134d6c1821"

# HMAC key for generating API tokens
API_SECRET = b"4B93C6C44D61C877FF58C7A5728C7"

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = client_secrets["web"]["client_id"]
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = client_secrets["web"]["client_secret"]

SOCIAL_AUTH_PIPELINE = (
        'social.pipeline.social_auth.social_details',
        'social.pipeline.social_auth.social_uid',
        'social.pipeline.social_auth.auth_allowed',
        'social.pipeline.social_auth.social_user',
        'social.pipeline.user.get_username',

        # Send a validation email to the user to verify its email address.
        # Disabled by default.
        # 'social.pipeline.mail.mail_validation',

        # Associates the current social details with another user account with
        # a similar email address. Disabled by default.
        # 'social.pipeline.social_auth.associate_by_email',

        'games.auth_pipeline.ask_username',
        'social.pipeline.user.create_user',
        'games.auth_pipeline.save_player_profile',
        'social.pipeline.social_auth.associate_user',
        'social.pipeline.social_auth.load_extra_data',
        'social.pipeline.user.user_details',
        'games.auth_pipeline.set_login_message',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

INTERNAL_IPS = ("127.0.0.1",)

ALLOWED_HOSTS = [
    ".heroku.com",
    ".herokuapp.com",
    "localhost",
]

AUTH_USER_MODEL = 'games.WsdGamesUser'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'games',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'wsd_games.urls'

WSGI_APPLICATION = 'wsd_games.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # FIXME: Enabling timezones leads to problems in SignupActivation.has_expired()

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "social.apps.django_app.context_processors.backends",
    "social.apps.django_app.context_processors.login_redirect",
    "games.context_processors.categories",
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

DOMAIN = "http://localhost:8000"

if "DYNO" in os.environ:
    #DEBUG = False
    DOMAIN = "http://wsd-games.herokuapp.com"
    ALLOWED_HOSTS = ['*']    
    STATIC_ROOT = 'staticfiles'
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()

if DEBUG:
    from django.contrib.messages import constants as message_constants
    MESSAGE_LEVEL = message_constants.DEBUG

LOGIN_URL = "/login"
LOGOUT_URL = "/logout"
LOGIN_REDIRECT_URL = "/"

PAYMENT_SUCCESS_URL = DOMAIN + "/payment/success"
PAYMENT_CANCEL_URL = DOMAIN + "/payment/cancel"
PAYMENT_ERROR_URL = DOMAIN + "/payment/error"

ACTIVATION_EXPIRATION_HOURS = 72
