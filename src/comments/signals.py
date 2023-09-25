from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from src.comments.models import Comment
from src.notifications.models import Notification


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, created, **kwargs):
    """create notification obejct if comment not root and user reply's not his own"""
    parent = instance.get_parent()
    if parent:
        created_at = instance.created_at
        reply_dtime = created_at.strftime("%A %d %b %Y %H:%M")
        text = f"Reply from {instance.user} {reply_dtime}: {instance.body}"
        if not instance.own_reply and not parent.deleted:
            Notification.objects.create(
                recipient=instance.reply_to,
                text=text,
                post=parent.post,
                parent_comment=parent,
            )
