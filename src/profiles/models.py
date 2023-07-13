import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from src.core.models import TimeStamp
from src.core.utils.base import upload_img
from src.core.utils.magic_valid_files import validate_img_mimetype
from src.profiles.managers import ProfileManager

User = get_user_model()


class Profile(TimeStamp):
    """
    In OneToOne relation with User Model
    """

    class Status(models.IntegerChoices):
        TRIALING = 1
        ACTIVE = 2
        EXEMPT = 3
        CANCELLED = 4
        TRIAL_EXPIRED = 5

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    avatar = models.ImageField(
        _("Avatar"),
        upload_to=upload_img,
        blank=True,
        null=True,
        validators=[validate_img_mimetype],
    )
    info = models.CharField(max_length=120, default="", blank=True)
    want_news = models.BooleanField(default=False, blank=True)
    status = models.IntegerField(
        choices=Status.choices, default=Status.EXEMPT, db_index=True, blank=True
    )
    objects = ProfileManager.as_manager()

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
