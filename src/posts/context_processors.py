from django.shortcuts import get_object_or_404
from django.urls import Resolver404, resolve, reverse

from src.posts.models.post_model import Post


def build_crumbs(request):
    """build breadcrumbs"""
    crumbs = [{"name": "Home", "url": reverse("home")}]
    try:
        match = resolve(request.path_info)
    except Resolver404:
        return {"crumbs": []}
    # if match.url_name == "post_list":
    crumbs.append({"name": "posts", "url": reverse("posts:post_list")})
    if match.url_name == "post_detail":
        post = get_object_or_404(Post, slug=match.kwargs["slug"])
        print(post)
        crumbs.append(
            {
                "name": post.title,
                "url": reverse(
                    f"{match.app_names[0]}:{match.url_name}",
                    args=[match.kwargs["slug"]],
                ),
            }
        )
    print("crumbs are ", crumbs)
    return {"crumbs": crumbs}
