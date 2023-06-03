import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from src.timestamp.models import TimeStamp
from src.timestamp.utils.base import upload_img
from src.timestamp.utils.magic_valid_files import validate_img_mimetype

User = get_user_model()


class Profile(TimeStamp):
    """
    In OneToOne relation with User Model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ?PROTECT
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    avatar = models.ImageField(
        _("Avatar"),
        upload_to=upload_img,
        blank=True,
        null=True,
        validators=[validate_img_mimetype],
    )
    info = models.CharField(max_length=120, default="", blank=True)

    def get_absolute_url(self):
        return reverse("profiles:profile_detail", kwargs={"uuid": self.uuid})

    def __str__(self) -> str:
        return self.user.username

    def delete(self):
        """if profile obj deleted; remove avatar file"""
        self.avatar.delete()
        super().delete()


class ProfileChart(Profile):
    class Meta:
        proxy = True
