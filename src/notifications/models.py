from functools import cached_property

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from src.comments.models import Comment
from src.posts.models.post_model import Post

User = get_user_model()


class NotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all_unread_notifics(self, recipient):
        return self.get_queryset().filter(recipient=recipient, read=False)

    def count_unread_notifics(self, recipient):
        return self.get_queryset().filter(recipient=recipient, read=False).count()

    def all_notifics(self, recipient):
        return self.get_queryset().filter(recipient=recipient)

    def get_first_five(self, recipient):
        return self.get_queryset().filter(recipient=recipient, read=False)[:5]

    def make_all_read(self, recipient):
        qs = self.get_queryset().filter(recipient=recipient, read=False)
        qs.update(read=True)


class Notification(models.Model):
    created = models.DateTimeField(default=now)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    read = models.BooleanField(default=False)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        Comment, null=True, blank=True, on_delete=models.SET_NULL
    )
    objects = NotificationManager()

    # @cached_property
    # def notifications_unread_count(self):
    #     return Notification.objects.filter(read=False).count()
    # @cached_property
    # def notifications(self):
    #     return Notification.objects.order_by('-id')[:5]
    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Notification for {self.recipient} | id={self.id}"
