"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/


"""

import os

from django.core.wsgi import get_wsgi_application

# should be adjusted for deploy


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.conf.dev")

if os.getenv("DJANGO_SETTINGS_MODULE"):
    os.environ["DJANGO_SETTINGS_MODULE"] = os.getenv("DJANGO_SETTINGS_MODULE")


application = get_wsgi_application()
