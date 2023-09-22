from django.urls import path

from .views import get_top_five, make_notifs_read

app_name = "notifications"

urlpatterns = [
    path("", get_top_five, name="all_notifics"),
    path("make-as-read/", make_notifs_read, name="mark_top_read"),
]
