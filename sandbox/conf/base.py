"""
django 4.2.1
"""


from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # let op: +parent
env = environ.Env(ALLOWED_HOSTS=(list, []), DEBUG=(bool, False))


environ.Env.read_env(BASE_DIR / ".env")


DEBUG = True
SECRET_KEY = env("SECRET_KEY")
SITE_ID = 1
AUTH_USER_MODEL = "accounts.User"

ALLOWED_HOSTS: list[str] = env("ALLOWED_HOSTS")
DJANGO_APPS = [
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.forms",
]

THIRD_PARTY = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "widget_tweaks",
    "django_htmx",
    "treebeard",
    "taggit",
    "django_extensions",
    # "modeltranslation", # see above
    "django_ckeditor_5",
    "rosetta",
    "captcha",
    "embed_video",
]


LOCAL_APPS = [
    "src.accounts.apps.AccountsConfig",
    "src.profiles.apps.ProfilesConfig",
    "src.posts.apps.PostsConfig",
    "src.core.apps.CoreConfig",
    "src.contacts.apps.ContactsConfig",
    "src.sentry.apps.SentryConfig",
    "src.comments.apps.CommentsConfig",
    "src.notifications.apps.NotificationsConfig",
    "src.devs.apps.DevsConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
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
                "src.contacts.context_processors.check_data_menu",
                "src.notifications.context_processors.check_nofications",
            ],
        },
    },
]

WSGI_APPLICATION = "sandbox.wsgi.application"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": env("DB_NAME"),
#         "USER": env("DB_USER"),
#         "PASSWORD": env("DB_PSW"),
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }


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


LANGUAGE_CODE = "en"
LANGUAGES = (("ru", _("Russian")), ("en", _("English")), ("uk", _("Ukrainian")))

USE_I18N = True
LOCALE_PATHS = (Path(BASE_DIR / "locale/"),)

TIME_ZONE = "UTC"
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
# auto-slug (trans)
autoslug_modeltranslation_enable = True

# clean widget
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# EMAIL

DEFAULT_FROM_EMAIL = "optima_helpdesk@zoo.com"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # dev.py


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

# taggit
TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING = True
TAGGIT_CASE_INSENSITIVE = True

# modeltranslation
MODELTRANSLATION_DEFAULT_LANGUAGE = "ru"
MODELTRANSLATION_LANGUAGES = (
    "ru",
    "en",
    "uk",
)

# sentry-sdk
SENTRY_ENABLED = False
# SENTRY_ENABLED = env("SENTRY_ENABLED")
SENTRY_DSN = "https://examplePublicKey@o0.ingest.sentry.io/0"


# django-ckeditor
CKEDITOR_FILENAME_GENERATOR = "src.core.utils.base.file_generate_name"

customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

# CKEDITOR_5_FILE_STORAGE = "blog.storage.CustomStorage"
# CKEDITOR_5_CUSTOM_CSS = STATIC_URL + "django_ckeditor_5/ckeditor_custom.css"
CKEDITOR_5_CUSTOM_CSS = "css/editor.css"  # optional
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "imageUpload",
        ],
    },
    "extends": {
        "language": "ru",
        "htmlSupport": {
            "allow": [
                {"name": "/.*/", "attributes": True, "classes": True, "styles": True}
            ]
        },
        # "link": {"addTargetToExternalLinks": "true"},
        # "mediaEmbed": {"previewsInData": "true"},
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "codeBlock",
            "sourceEditing",
            "insertImage",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "imageUpload",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
    },
    "list": {
        "properties": {
            "styles": "true",
            "startIndex": "true",
            "reversed": "true",
        }
    },
}

USE_CAPCHA = True
# RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
# RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")
SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]


# AWS

# AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# AWS_QUERYSTRING_AUTH = False  # key will be not present in url
# AWS_S3_MAX_MEMORY_SIZE = 2200000
# AWS_S3_REGION_NAME = "eu-central-1"
