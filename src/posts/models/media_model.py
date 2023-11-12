# from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from embed_video.fields import EmbedVideoField

from src.core.models import MediaStamp
from src.core.utils.base import upload_img


class Video(MediaStamp):
    """
    note for templates:
    load tag
    {% video item.url '426x240' %} {{item.title}}
    let op: title,added_at (abstract MediaStamp)
    """

    class ImageCategory(models.IntegerChoices):
        SINGLE = 0, _("first")
        GENERAL = 1, _("not_specified")
        ENDO = 2, _("endo")
        CARDIO = 3, _("cardio")
        GI = 4, _("gastro")
        IM = 5, _("immune")
        URO = 6, _("uro_gen")
        NEURO = 7, _("neuro")
        TOXI = 8, _("toxic")
        OLD = 9, _("old")
        __empty__ = _("(Unknown)")

    url = EmbedVideoField()
    # check obj.EMBED_VIDEO_YOUTUBE_CHECK_THUMBNAIL
    thumbnail = models.ImageField(upload_to=upload_img, null=True, blank=True)
    categ = models.IntegerField(
        choices=ImageCategory.choices, default=ImageCategory.GENERAL
    )

    def save(self, *args, **kwargs):
        """auto create datetime if public status changes"""
        self.created = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Video {self.id}"

    # https://youtu.be/jQ_KTIY5XJo?list=PLP08XsLK51Qxpz8Rp5hGH09_jTCBRoVAE
