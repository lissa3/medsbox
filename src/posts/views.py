from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from src.posts.models.post_model import Post


class PostList(ListView):
    """display only public posts"""

    template_name = "posts/post_list.html"
    context_object_name = "posts"

    paginate_by = 2

    def get_queryset(self):
        return (
            Post.objects.get_public()
            .select_related("categ", "author")
            .prefetch_related("tags")
        )


class PostTagSearch(ListView):
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        """slug in ASCII"""
        tag = self.kwargs.get("tag")
        return Post.objects.get_public().filter(tags__slug__in=[tag])
