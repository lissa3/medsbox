from django import template

from src.posts.models.categ_model import Category

register = template.Library()


@register.inclusion_tag("components/categ_bar.html")
def show_categs(**kwargs):
    """substitute template sidebar with root categs"""
    categs = Category.get_root_nodes()
    return {"categs": categs, **kwargs}
