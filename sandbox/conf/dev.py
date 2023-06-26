from .base import *  # noqa

INTERNAL_IPS = ["127.0.0.1"]
INSTALLED_APPS += ["django_extensions"]

# use in-memory-db

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "memory",
    }
}
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
