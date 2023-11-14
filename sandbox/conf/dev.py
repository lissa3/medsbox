from .base import *  # noqa

INTERNAL_IPS = ["127.0.0.1"]
ABSOLUTE_URL_BASE = "http://127.0.0.1:8000"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "comms",
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PSW"),
        "HOST": "localhost",
        "PORT": "5432",
    }
}
# use in-memory-db
# let op: email confirmation will be NOT in console
# EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


USE_CAPCHA = False
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "dj": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 1,  # 1MB
            "backupCount": 5,
            "filename": "zoo/django_native.log",
        },
        "upload_problems": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024 * 1024 * 1,
            "backupCount": 5,
            "formatter": "verbose",
            "filename": "zoo/upload.log",
        },
        "users": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024 * 1024 * 1,
            "backupCount": 5,
            "formatter": "verbose",
            "filename": "zoo/user_issues.log",
        },
        "mail_admin": {
            "level": "CRITICAL",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            # 'handlers': ['dj','console'],
            # 'handlers': ['mail_admin','dj'],
            "level": "WARNING",
            "propagate": False,
        },
        "upload": {
            "handlers": ["upload_problems"],
            "level": "WARNING",
        },
        "user_issues": {
            "handlers": ["users"],
            "level": "INFO",
        },
    },
}
