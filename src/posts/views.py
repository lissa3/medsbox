from django.http import HttpResponseForbidden
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
from src.posts.models.categ_model import Category
from src.posts.models.post_model import Post

from .mixins import CategoryCrumbMixin, PostListMenuMixin


class PostList(PostListMenuMixin, ListView):

    """display only public posts"""

    template_name = "posts/post_list.html"
    context_object_name = "posts"

    paginate_by = 2

    def get_queryset(self):
        # print("looking for posts")
        return Post.objects.get_public().prefetch_related("tags")


class PostDetail(CategoryCrumbMixin, DetailView):
    model = Post
    form_class = CommentForm
    template_name = "posts/post_detail.html"

    def get_context_data(self, **kwargs):
        comms = Comment.objects.exists()
        ctx = super().get_context_data(**kwargs)
        ctx["cats_path"] = self.get_post_categs_path()
        ctx["comments"] = comms
        form = CommentForm()
        ctx["form"] = form
        return ctx


class PostCommFormView(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = "posts/post_detail.html"

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comm = form.save(commit=False)
            comm.user = request.user
            comm.post = self.object
            Comment.add_root(instance=comm)
            return self.form_valid(form)
        else:
            print("form invalid")
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


class PostTagSearch(PostListMenuMixin, ListView):
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        """slug in ASCII"""
        tag = self.kwargs.get("tag")
        return Post.objects.get_public().filter(tags__slug__in=[tag])


class PostCategSearch(PostListMenuMixin, ListView):
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
            # given categ has no kids
            return Post.objects.get_public().filter(categ_id=categ.id)


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
