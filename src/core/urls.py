from django.urls import path

from .views import home, intro

app_name = "core"

urlpatterns = [
    path("", home, name="home"),
    path("general-info/", intro, name="intro"),
]
