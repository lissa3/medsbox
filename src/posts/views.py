from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from src.posts.models.categ_model import Category
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


class PostCategSearch(ListView):
    """retrieve all posts linked to a given category"""

    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        """filter public post for a given category(and it's categ descendants)"""
        slug = self.kwargs.get("slug")
        categ = get_object_or_404(Category, slug=slug)
        categ_descend = categ.get_descendants()
        if categ_descend:
            return Post.objects.get_public().filter(categ__in=categ_descend)
        else:
            print("given categ has no kids")
            lst = Post.objects.get_public()
            for post in lst:
                print(post.categ)
            return Post.objects.get_public().filter(categ_id=categ.id)
            # return Post.objects.get_public().filter(categ__slug=slug)
