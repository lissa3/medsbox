from django.urls import path, re_path

from .views import PostList, PostTagSearch

app_name = "posts"

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    re_path(
        r"^tag-search/(?:t:(?P<tag>[-\w]+)/)?$",
        PostTagSearch.as_view(),
        name="tag_search",
    ),
]
