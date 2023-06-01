"""
django 4.2.1
"""

from pathlib import Path

import environ

env = environ.Env(ALLOWED_HOSTS=(list, []), DEBUG=(bool, False))


BASE_DIR = Path(__file__).resolve().parent.parent.parent  # let op: +parent
environ.Env.read_env(BASE_DIR / ".env")


DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY")


ALLOWED_HOSTS: list[str] = env("ALLOWED_HOSTS")
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]


LOCAL_APPS = [
    "src.accounts.apps.AccountsConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sandbox.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "src" / "templates"],
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

WSGI_APPLICATION = "sandbox.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.\
        MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.\
        CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.\
        NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
# STATIC_ROOT = BASE_DIR / "src" / "static"
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR.joinpath("src", "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.joinpath("media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
