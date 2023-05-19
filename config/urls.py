"""config URL Configuration 4.1"""
# import os

from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path(os.getenv('SECRET_ADMIN_URL') + '/admin/', admin.site.urls),
    path("admin/", admin.site.urls),
]
