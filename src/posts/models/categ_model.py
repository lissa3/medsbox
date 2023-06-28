from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

from src.core.utils.base import upload_img


class Category(MP_Node):
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from="name", unique=True)
    icon = models.ImageField(
        verbose_name=_("Icon"), null=True, blank=True, upload_to=upload_img
    )

    node_order_by = ["name"]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"Category: {self.name}"

    def get_full_path(self):
        if self.is_root():
            path_slug = self.slug
        else:
            path_slug = "/".join(
                list(self.get_ancestors().values_list("slug", flat=True))
            )
            path_slug += f"/{self.slug}"
        return path_slug

    # def get_absolute_url(self):
    #     """for bread crumbs UI"""
    #     return reverse("products:cat_detail", kwargs={"slug": self.get_full_path()})


#  C.dump_bulk()
# C.get_annotated_list()
"""

>>> zoo = Category.get_annotated_list()
>>> pprint(zoo)
[(<Category: Comps>, {'close': [], 'level': 0, 'open': True}),
 (<Category: desktop>, {'close': [], 'level': 1, 'open': True}),
 (<Category: tablet>, {'close': [0, 1], 'level': 1, 'open': False})]
>>>

"""
