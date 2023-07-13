from .base import *  # noqa

INTERNAL_IPS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "memory",
    }
}
# use in-memory-db
# let op: email confirmation will be NOT in console
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
