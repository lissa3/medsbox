import uuid

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from unidecode import unidecode  # noqa

# from src.contacts.models import NewsLetter
from src.core.models import TimeStamp
from src.core.utils.base import upload_img
from src.posts.managers import PostFilterManager
from src.posts.models.categ_model import Category

User = get_user_model()


class Post(TimeStamp):
    """pivotal model;"""

    class CurrentStatus(models.IntegerChoices):
        DRAFT = 0, _("drafts")
        REVIEW = 1, _("reviews")
        PUB = 2, _("published")

    class SendingStatus(models.IntegerChoices):
        PENDING = 0, _("pend")
        READY = 1, _("to send")
        SENT = 2, _("sent")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title", unique=True, editable=True, blank=True)
    categ = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=Category.get_default_pk,
    )
    content = models.TextField()
    top_img = models.ImageField(upload_to=upload_img, null=True, blank=True)
    url_top_img = models.URLField(blank=True, default="")
    status = models.IntegerField(
        choices=CurrentStatus.choices, default=CurrentStatus.DRAFT, blank=True
    )
    is_deleted = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    featured = models.BooleanField(blank=True, default=False)
    allow_comments = models.BooleanField(default=True)
    send_status = models.IntegerField(
        choices=SendingStatus.choices, default=SendingStatus.PENDING, blank=True
    )
    letter = models.ForeignKey(
        "contacts.NewsLetter",
        related_name="posts",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    tags = TaggableManager(
        blank=True, verbose_name="Tags", help_text="Tags should be separated by comma"
    )
    objects = PostFilterManager.as_manager()

    def soft_delete(self):
        """soft  delete a model instance"""
        self.is_deleted = True
        self.save()

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        assert self.slug
        return reverse("posts:detail_post", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return f"{self.title} | {self.author}"
