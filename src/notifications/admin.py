from django.contrib import admin

from src.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """display notifications list"""

    list_display = (
        "id",
        "created",
        "recipient",
        "read",
    )
    list_filter = ("created", "recipient")
    list_display_links = ["recipient"]
    date_hierarchy = "created"
