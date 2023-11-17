from django.urls import path

from .views import about, intro, thanks

app_name = "core"

urlpatterns = [
    path("general-info/", intro, name="intro"),
    path("acknowledgments/", thanks, name="thanks"),
    path("about/", about, name="about"),
]
