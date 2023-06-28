"""
django 4.2.1
"""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # let op: +parent
env = environ.Env(ALLOWED_HOSTS=(list, []), DEBUG=(bool, False))


environ.Env.read_env(BASE_DIR / ".env")


DEBUG = True
SECRET_KEY = env("SECRET_KEY")
SITE_ID = 1
AUTH_USER_MODEL = "accounts.User"

ALLOWED_HOSTS: list[str] = env("ALLOWED_HOSTS")
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.forms",
]

THIRD_PARTY = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "widget_tweaks",
    "django_htmx",
    "django_extensions",
    "treebeard",
]


LOCAL_APPS = [
    "src.accounts.apps.AccountsConfig",
    "src.profiles.apps.ProfilesConfig",
    "src.posts.apps.PostsConfig",
    "src.core.apps.CoreConfig",
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
    "django_htmx.middleware.HtmxMiddleware",
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
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
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

################################
#                extra's
################################

# clean widget
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# EMAIL

DEFAULT_FROM_EMAIL = "optima_helpdesk@zoo.com"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_BACKEND = env("EMAIL_BACKEND")
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend" # dev.py


# img upload limits

MIN_UPLOAD_SIZE = 120  # in bytes
MAX_UPLOAD_SIZE = 1024 * 1024 * 2  # 2 MB
UPLOAD_FILE_TYPES = "image/jpeg,image/png,image/jpg"
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 2  # for MemFileUploadHandler info


# allauth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


ACCOUNT_FORMS = {
    "signup": "src.accounts.forms.CustomSignupForm",
}
ACCOUNT_ADAPTER = "src.accounts.adapters.InactiveUserEmailAdapter"


ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_AUTHENTICATION_METHOD = "email"  # can be both
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # "optional"
ACCOUNT_USERNAME_MIN_LENGTH = 3
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/login"

# ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 5
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Help  desk - "
ACCOUNT_USERNAME_BLACKLIST = ["admin", "administrator", "moderator"]
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_USERNAME_BLACKLIST = []
