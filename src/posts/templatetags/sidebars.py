from django import template
from taggit.models import Tag

from src.posts.models.categ_model import Category

register = template.Library()


@register.inclusion_tag("components/categ_bar.html")
def show_categs(**kwargs):
    """substitute template sidebar with root categs"""
    categs = Category.get_root_nodes()
    return {"categs": categs}


@register.inclusion_tag("components/tags.html")
def show_tags():
    """substitute template sidebar with tags"""
    tags = Tag.objects.all()
    return {"tags": tags}
