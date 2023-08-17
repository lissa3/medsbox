from django.urls import path, re_path

from .views import PostCategSearch, PostList, PostTagSearch

app_name = "posts"

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path("categ/<slug:slug>/", PostCategSearch.as_view(), name="cat_search"),
    re_path(
        r"^tag-search/(?:t:(?P<tag>[-\w]+)/)?$",
        PostTagSearch.as_view(),
        name="tag_search",
    ),
]
