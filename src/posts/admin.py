from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from modeltranslation.admin import TranslationAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from src.core.utils.admin_help import admin_link
from src.posts.models.categ_model import Category
from src.posts.models.post_model import Post


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)
    list_display = ["name", "slug"]
    ordering = ["path"]


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    """
    author field for current user;
    user== staff can crud only their own objects
    """

    date_hierarchy = "created_at"
    search_fields = ("title", "categ__name")

    list_display = [
        # "id",
        "title",
        "author",
        "status",
        "is_deleted",
        "show_img",
        "display_tags",
        "categ_link",
    ]
    list_select_related = ("categ", "author")
    list_select_related = ("categ", "author")
    list_editable = ["is_deleted"]
    list_display_links = ["title"]
    list_filter = ["status", "created_at"]
    radio_fields = {"status": admin.HORIZONTAL}
    save_on_top = True
    list_filter = ["status", "created_at", "is_deleted"]
    list_per_page = 15
    actions = ("make_posts_published",)
    empty_value_display = "No data"

    @admin.action(description="Mark as published")
    def make_posts_published(self, request, queryset):
        """make possbile to mark posts as published in admin bar checkbox"""
        updated = queryset.update(status=2)
        self.message_user(
            request,
            ngettext(
                "%d successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    def get_queryset(self, request):
        """
        super user can crud all posts;
        user is_staff can crud only their own objetcs
        """
        initial_qs = super().get_queryset(request).prefetch_related("tags")
        if request.user.is_superuser:
            return initial_qs
        return initial_qs.filter(author=request.user)

    def show_img(self, obj):
        """if top_img show small thumbnail in admin table"""
        if obj.top_img:
            return format_html("<img src={} width='60' />", obj.top_img_url)
        # return format_html("<a href={}>{}</a>", url, func(self, related_obj))
        # if obj.top_img:
        #     return mark_safe(f"<img src=`!r{obj.top_img_url}` width='60' />")

    def display_tags(self, obj):
        """if tags make a flat list of them"""
        tags_list = obj.tags.all().values_list("name", flat=True)
        return ", ".join(tags_list)

    # new feature: adjust admin (see three func below)
    # current admin will be auto-selected in add post view
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """add current admin kwargs"""
        if db_field.name == "author":
            kwargs["queryset"] = get_user_model().objects.filter(
                username=request.user.username
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        """
        prevent more than 1 author choice;
        author field will be current user from request
        """
        if obj is not None:
            return self.readonly_fields + ("author",)
        return self.readonly_fields

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data["author"] = request.user
        request.GET = data
        return super().add_view(request, form_url="", extra_context=extra_context)

    # new feature: adjust admin (see two func below)
    # using link to access related categ object

    def admin_change_url(self, obj: object):
        """
        help func: buil-in schema for detail view (any admin model obj)"""

        app_label = obj._meta.app_label
        model_name = obj._meta.model.__name__.lower()
        return reverse(f"admin:{app_label}_{model_name}_change", args=(obj.pk,))

    @admin_link("categ", _("Category"))
    def categ_link(self, categ: object):
        return categ
