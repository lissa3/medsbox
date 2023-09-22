from django.db.models.signals import post_save
from django.dispatch import receiver

from src.accounts.admin import User
from src.notifications.models import Notification


@receiver(post_save, sender=User)
def send_notification(instance, **kwargs):
    # check if comment is on own comment; UI allows it but no notifications
    parent = instance.get_parent()
    if parent and parent.user.username != instance.user.username:
        sender = (instance.user,)
        recipient = (instance.reply_to,)
        Notification.objects.create(
            recipient=recipient,
            sender=sender,
            text=f"You've got a comment from {sender} written at {instance.created}",
        )
