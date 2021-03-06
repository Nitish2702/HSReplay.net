"""
Django settings for hsreplay.net project.
"""

import os
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IS_RUNNING_AS_LAMBDA = bool(os.environ.get("IS_RUNNING_AS_LAMBDA", ""))
IS_RUNNING_LIVE = os.uname()[1] == "hearthsim.net"

ROOT_URLCONF = "hsreplaynet.urls"
WSGI_APPLICATION = "wsgi.application"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "be8^qa&f2fut7_1%q@x2%nkw5u=-r6-rwj8c^+)5m-6e^!zags"

if IS_RUNNING_LIVE or IS_RUNNING_AS_LAMBDA:
	DEBUG = False
	ALLOWED_HOSTS = ["hsreplay.net", "www.hsreplay.net"]
else:
	# SECURITY WARNING: don't run with debug turned on in production!
	DEBUG = True
	ALLOWED_HOSTS = []


INSTALLED_APPS = [
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	"django.contrib.sites",
	"rest_framework",
	"hsreplaynet.accounts",
	"hsreplaynet.api",
	"hsreplaynet.cards",
	"hsreplaynet.games",
	"hsreplaynet.lambdas",
	"hsreplaynet.scenarios",
	"hsreplaynet.stats",
	"hsreplaynet.uploads",
	"hsreplaynet.utils",
]

if not IS_RUNNING_AS_LAMBDA:
	INSTALLED_APPS += [
		"django.contrib.flatpages",
		"allauth",
		"allauth.account",
		"allauth.socialaccount",
		"allauth_battlenet",
		"loginas",
	]

if not DEBUG:
	INSTALLED_APPS += [
		"raven.contrib.django.raven_compat",
	]


MIDDLEWARE_CLASSES = (
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
	"django.middleware.security.SecurityMiddleware",
	"django.middleware.gzip.GZipMiddleware",
)

TEMPLATES = [{
	"BACKEND": "django.template.backends.django.DjangoTemplates",
	"DIRS": [
		os.path.join(BASE_DIR, "hsreplaynet", "templates")
	],
	"APP_DIRS": True,
	"OPTIONS": {
		"context_processors": [
			"django.template.context_processors.debug",
			"django.template.context_processors.request",
			"django.contrib.auth.context_processors.auth",
			"django.contrib.messages.context_processors.messages",
		],
	},
}]


# Tests

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
FIXTURE_DIRS = (os.path.join(BASE_DIR, "hsreplaynet", "test", "fixtures"), )


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "hsreplaynet", "static"),
]

if DEBUG:
	DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
	STATIC_URL = "/static/"
else:
	DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
	STATICFILES_STORAGE = "whitenoise.django.GzipManifestStaticFilesStorage"
	STATIC_URL = "https://static.hsreplay.net/static/"

	# S3
	S3_RAW_LOG_STORAGE_BUCKET = os.environ.get(
		"S3_RAW_LOG_STORAGE_BUCKET",
		"test.raw.replaystorage.hsreplay.net"
	)
	S3_REPLAY_STORAGE_BUCKET = os.environ.get(
		"S3_REPLAY_STORAGE_BUCKET",
		"test.replaystorage.hsreplay.net"
	)
	AWS_STORAGE_BUCKET_NAME = S3_REPLAY_STORAGE_BUCKET

	AWS_S3_USE_SSL = True
	AWS_DEFAULT_ACL = "private"

	AWS_IS_GZIPPED = True
	GZIP_CONTENT_TYPES = (
		"text/xml",
		"text/plain",
		"application/xml",
		"application/octet-stream",
	)

JOUST_STATIC_URL = STATIC_URL + "joust/"
HEARTHSTONEJSON_URL = "https://cdn.hearthstonejson.com/v1/%(build)s/%(locale)s/cards.json"


# Email
# https://docs.djangoproject.com/en/1.9/ref/settings/#email-backend

SERVER_EMAIL = "admin@hsreplay.net"
DEFAULT_FROM_EMAIL = "contact@hsreplay.net"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.sqlite3",
		"NAME": os.path.join(BASE_DIR, "db.sqlite"),
		"USER": "",
		"PASSWORD": "",
		"HOST": "",
		"PORT": "",
	}
}


# Logging


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = "en-us"

USE_TZ = True
TIME_ZONE = "UTC"

SITE_ID = 1


# Account settings

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = (
	# Needed to login by username in Django admin, regardless of `allauth`
	"django.contrib.auth.backends.ModelBackend",
	# `allauth` specific authentication methods, such as login by e-mail
	"allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_REDIRECT_URL = reverse_lazy("my_replays")
LOGIN_URL = reverse_lazy("account_login")

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" if DEBUG else "https"
SOCIALACCOUNT_ADAPTER = "allauth_battlenet.provider.BattleNetSocialAccountAdapter"
SOCIALACCOUNT_PROVIDERS = {"battlenet": {"SCOPE": []}}


# API
REST_FRAMEWORK = {
	# Use Django's standard `django.contrib.auth` permissions,
	# or allow read-only access for unauthenticated users.
	"DEFAULT_PERMISSION_CLASSES": [
		"rest_framework.permissions.IsAuthenticatedOrReadOnly",
	]
}


# Custom site settings

# HDT_DOWNLOAD_URL = "https://hsdecktracker.net"
# Swap when we're in public beta
HDT_DOWNLOAD_URL = "https://hsreplay.net/pages/beta/"


try:
	from hsreplaynet.local_settings import *
except ImportError:
	pass
