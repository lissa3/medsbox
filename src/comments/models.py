import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

from src.core.models import TimeStamp
from src.posts.models.post_model import Post

User = get_user_model()


class Comment(TimeStamp, MP_Node):
    """TODO: add func banned users;
    own_reply (users replyed to themselves)
    """

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, related_name="comments", on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=2000)
    banned = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="reply_ers",
    )
    own_reply = models.BooleanField(default=False)

    # node_order_by = ["path"]  # defines sorted<->unsorted in create form

    class Meta:
        ordering = ("path",)

    def __str__(self):
        return f"Body: {self.body}"

    # TODO: add time delta : created_at  == updated_at for edit
    @property
    def mark_edited(self):
        return self.created_at != self.updated_at

    @property
    def depth_limit(self):
        """help for UI rendering: nested depth limit for indentaion to left"""
        return self.depth < 2
