from django.urls import path, re_path

from .views import PostCategSearch, PostDetail, PostList, PostTagSearch, SearchPost

app_name = "posts"

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path("detail/<slug:slug>/", PostDetail.as_view(), name="post_detail"),
    path("categ/<slug:slug>/", PostCategSearch.as_view(), name="cat_search"),
    path("search/", SearchPost.as_view(), name="search_posts"),
    re_path(
        r"^tag-search/(?:t:(?P<tag>[-\w]+)/)?$",
        PostTagSearch.as_view(),
        name="tag_search",
    ),
]
