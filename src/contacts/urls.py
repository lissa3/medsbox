from django.urls import path

from .views import Subscribe, UnSubscribe

app_name = "contacts"

urlpatterns = [
    path("subscribe/", Subscribe.as_view(), name="subscribe"),
    path("unsubscribe/<uuid:uuid>/", UnSubscribe.as_view(), name="end_news"),
]
