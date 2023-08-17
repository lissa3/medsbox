from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

from src.core.utils.base import upload_img


class Category(MP_Node):
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from="name", unique=True)
    icon = models.ImageField(
        verbose_name=_("Icon"), null=True, blank=True, upload_to=upload_img
    )

    node_order_by = ["name"]  # defines sorted<->unsorted in create form

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    @classmethod
    def get_default_pk(cls, *args, **kwargs):
        """create or use existed default category"""
        qs = cls.objects.filter(name=_("Неопределена"))
        try:
            obj = qs.get()
        except qs.model.DoesNotExist:
            cls.add_root(name=_("Неопределена"))
            obj = cls.objects.get(name=_("Неопределена"))
        # obj, _ = cls.objects.get_or_create(name="Unspecified")
        return obj.pk

    def get_full_path(self):
        if self.is_root():
            path_slug = self.slug
        else:
            path_slug = "/".join(
                list(self.get_ancestors().values_list("slug", flat=True))
            )
            path_slug += f"/{self.slug}"
        return path_slug

    def __str__(self):
        return f"Category: {self.name}"
