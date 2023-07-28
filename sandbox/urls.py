"""config URL Configuration 4.1"""
# import os

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from src.core.views import home

# from django.views.generic import TemplateView

urlpatterns = [
    # path(eve('SECRET_ADMIN_URL') + '/admin/', admin.site.urls),
    path(
        "i18n/",
        include("django.conf.urls.i18n"),
    ),
    path("admin/", admin.site.urls),
]

urlpatterns += i18n_patterns(
    path("", home, name="home"),
    path("accounts/", include("allauth.urls")),
    path("core/", include("src.core.urls")),
    path("profile/", include("src.profiles.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
