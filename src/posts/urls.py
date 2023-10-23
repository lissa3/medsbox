from django.urls import path, re_path

from src.posts.views.post_views import (
    PostCategSearch,
    PostComment,
    PostDatumFilter,
    PostList,
    PostTagSearch,
    SearchPost,
)
from src.posts.views.user_action_views import track_like

app_name = "posts"

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path("detail/<slug:slug>/", PostComment.as_view(), name="post_detail"),
    path("categ/<slug:slug>/", PostCategSearch.as_view(), name="cat_search"),
    path("search/", SearchPost.as_view(), name="search_posts"),
    re_path(
        r"^tag-search/(?:t:(?P<tag>[-\w]+)/)?$",
        PostTagSearch.as_view(),
        name="tag_search",
    ),
    path(
        "comments/<slug:slug>/<thread_uuid>/", PostComment.as_view(), name="get_branch"
    ),
    path(
        "datum-filter/<year>/<month>/",
        PostDatumFilter.as_view(),
        name="filter_calend",
    ),
]

htmx_urlpatterns = [
    path("interaction/", track_like, name="track_likes"),
]
urlpatterns += htmx_urlpatterns
