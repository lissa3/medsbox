from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, FormView, ListView, View
from django.views.generic.detail import SingleObjectMixin

from src.comments.forms import CommentForm
from src.comments.models import Comment
from src.core.utils.views_help import make_query, search_qs
from src.posts.forms import SearchForm
from src.posts.mixins import CategoryCrumbMixin, PostListMenuMixin
from src.posts.models.categ_model import Category
from src.posts.models.post_model import Post
from src.posts.models.relation_model import Relation


class PostList(PostListMenuMixin, ListView):
    """display only public posts"""

    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return (
            Post.objects.get_public().prefetch_related("tags").order_by("-published_at")
        )


class PostDetail(CategoryCrumbMixin, DetailView):
    """
    Detail view to display post object with comments;
    ability to check comments tools via template
    """

    model = Post
    form_class = CommentForm
    template_name = "posts/post_detail.html"
    _thread_uuid = None

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post.objects.get_public(), slug=self.kwargs.get("slug")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # print("full path is",self.request.get_full_path())
        if self.request.user.is_authenticated:
            # populate ctx with initial bools: user's likes and bmark for UI
            _post = self.get_object()
            _user = self.request.user
            try:
                rel_obj = Relation.objects.get(post=_post, user=_user)
                # bools for UI: current state for likes
                if rel_obj.like:
                    ctx["liked"] = True
                if rel_obj.in_bookmark:
                    ctx["display_bmark_button"] = False
                else:
                    ctx["display_bmark_button"] = True

            except Relation.DoesNotExist:
                ctx.update({"display_bmark_button": True, "liked": False})

        comms = Comment.objects.filter(post=self.get_object()).exists()
        ctx["cats_path"] = self.get_post_categs_path()
        ctx["comments"] = comms
        if self._thread_uuid:
            ctx["thread_uuid"] = self._thread_uuid
        if comms:
            ctx["comms_total"] = Comment.objects.filter(post=self.get_object()).count()
        form = CommentForm()
        ctx["form"] = form
        return ctx

    def dispatch(self, *args, **kwargs):
        #  all related comments or selected thread (via notifications);
        self._thread_uuid = kwargs.pop("thread_uuid", None)
        return super().dispatch(*args, **kwargs)


class PostCommFormView(LRM, SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = "posts/post_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comm = form.save(commit=False)
            comm.user = request.user
            comm.post = self.object
            Comment.add_root(instance=comm)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("posts:post_detail", kwargs={"slug": self.object.slug})


class PostComment(View):
    def get(self, request, *args, **kwargs):
        view = PostDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommFormView.as_view()
        return view(request, *args, **kwargs)


class PostDatumFilter(ListView):
    context_object_name = "posts"
    paginate_by = 2
    _year = None
    _month = None
    ordering = ["-published_at"]

    def get_queryset(self):
        return (
            Post.objects.get_public()
            .filter(published_at__year=self._year, published_at__month=self._month)
            .order_by("-published_at")
        )

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return "posts/parts/posts_collection.html"
        else:
            return "posts/post_list.html"

    def dispatch(self, *args, **kwargs):
        self._year = kwargs.pop("year", None)
        str_month = kwargs.pop("month", None)
        self._month = str_month.split("-")[1]
        return super().dispatch(*args, **kwargs)


class PostTagSearch(PostListMenuMixin, ListView):
    context_object_name = "posts"
    paginate_by = 2
    _tag = None

    def get_queryset(self):
        """slug in ASCII"""
        tag = self.kwargs.get("tag")
        self._tag = tag
        return (
            Post.objects.get_public()
            .filter(tags__slug__in=[tag])
            .order_by("-published_at")
        )

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return "posts/parts/posts_collection.html"
        else:
            return "posts/post_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["count_total"] = self.get_queryset().count()
        ctx["tag"] = self._tag
        return ctx


class PostCategSearch(PostListMenuMixin, ListView):
    """retrieve all posts linked to a given category"""

    context_object_name = "posts"
    paginate_by = 5
    ordering = ["-published_at"]
    _slug = None

    def get_queryset(self):
        """filter public post for a given category(and it's categ descendants)"""
        slug = self.kwargs.get("slug")
        self._slug = slug
        categ = get_object_or_404(Category, slug=slug)

        _tree_categs = categ.get_tree(categ)
        if _tree_categs:
            return (
                Post.objects.get_public()
                .filter(categ__in=_tree_categs)
                .order_by("-published_at")
            )
        else:
            return Post.objects.none()

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return "posts/parts/posts_collection.html"
        else:
            return "posts/post_list.html"

    def get_context_data(self, **kwargs):
        # add attr `_slug` for pagination based on htmx
        ctx = super().get_context_data(**kwargs)
        ctx["count_total"] = self.get_queryset().count()
        ctx["slug"] = self._slug
        return ctx


class SearchPost(PostListMenuMixin, ListView):
    """
    search ru and en: via vector_ru,vector_en(triggers in migration files)
    search in ukrainian: via model manager(no config in this lang)
    """

    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 5
    empty_flag = False
    not_found_flag = False
    inp_errors = None

    def get_queryset(self, *args, **kwargs):
        form = SearchForm(self.request.GET)

        current_lang = get_language()
        if form.is_valid():
            lang = form.cleaned_data.get("lang", current_lang)
            q = form.cleaned_data.get("q", None)

            if q is not None:
                if len(q) >= 1:
                    query = make_query(lang, q)
                    posts = search_qs(lang, query=query)
                    if posts.count() >= 1:
                        return posts
                    else:
                        self.not_found_flag = True
                        return Post.objects.none()
                else:
                    # raise Http404('Send a search term')
                    self.empty_flag = True
                    return Post.objects.none()
        else:
            self.inp_errors = form.errors
            return Post.objects.none()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        posts = self.get_queryset()
        if posts:
            context["posts"] = posts
            context["count"] = posts.count()
        elif self.empty_flag:
            context["empty_flag"] = _("You sent no search word(s)")
        elif self.inp_errors:
            context["invalid_input"] = _("Query is invalid")
        return context


class PostBookMarkCollection(LRM, ListView):
    template_name = "posts/post_bmarks.html"
    context_object_name = "posts"
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        users_with_rels = user.user_rel.filter(in_bookmark=True).values_list(
            "post_id", flat=True
        )
        return Post.objects.get_public().filter(id__in=users_with_rels)
