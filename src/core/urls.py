from django.urls import path

from .views import intro

app_name = "core"

urlpatterns = [
    path("general-info/", intro, name="intro"),
]
