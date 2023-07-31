from django.db import models
from django.utils.translation import gettext_lazy as _

from src.core.models import MediaStamp


class NewsLetter(MediaStamp):
    """
    TODO: link and view unsubscribe;
    add a comment about fallback lang and
    ask to help with translations;
    post can be NULL (letter without post link)
    """

    class Status(models.IntegerChoices):
        PENDING = 0, _("pending")
        READY = 1, _("ready to send")
        SENT = 2, _("sent")

    text = models.TextField(default="", blank=True)
    letter_status = models.IntegerField(
        choices=Status.choices, default=Status.PENDING, blank=True
    )
    sended_at = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Letter #id {self.id}"
