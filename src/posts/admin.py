from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django_ckeditor_5.widgets import CKEditor5Widget
from modeltranslation.admin import TranslationAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from src.contacts.models import NewsLetter
from src.core.utils.admin_help import admin_link
from src.posts.models.categ_model import Category
from src.posts.models.post_model import Post


@admin.register(Category)
class CategoryAdmin(TreeAdmin, TranslationAdmin):
    form = movenodeform_factory(Category)
    list_display = ["name", "slug"]
    list_display_links = ["name"]
    ordering = ["path"]


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    """
    ordering based on model('-created_at')

    """

    date_hierarchy = "created_at"
    search_fields = ("title", "categ__name")

    list_display = [
        "id",
        # "author",
        "title",
        "status",
        "is_deleted",
        # "show_img",
        "published_at",
        "display_tags",
        "categ_link",
    ]
    list_select_related = ("categ", "author")
    list_editable = ["is_deleted"]  # , "status"]
    list_display_links = ["title"]
    list_filter = ["status", "created_at"]
    radio_fields = {"status": admin.HORIZONTAL}
    save_on_top = True
    list_filter = ["status", "created_at", "is_deleted"]
    list_per_page = 15
    actions = ("make_posts_published", "set_to_draft", "set_to_review")
    empty_value_display = " --- # ---"
    formfield_overrides = {
        models.TextField: {"widget": CKEditor5Widget(config_name="extends")},
    }

    @admin.action(description="to_public")
    def make_posts_published(self, request, queryset):
        """make possbile to mark posts as published in admin bar checkbox"""
        updated = queryset.update(status=2, published_at=timezone.now())

        self.message_user(
            request,
            ngettext(
                "%d post successfully marked as published.",
                "%d posts were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description="to_review")
    def set_to_review(self, request, queryset):
        """make possbile to mark posts as published in admin bar checkbox"""
        updated = queryset.update(status=1, published_at=timezone.now())

        self.message_user(
            request,
            ngettext(
                "%d post successfully marked as published.",
                "%d posts were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description="to_draft")
    def set_to_draft(self, request, queryset):
        """make possbile to undo published status"""
        updated = queryset.update(status=0, published_at=None)

        self.message_user(
            request,
            ngettext(
                "%d post successfully marked as draft.",
                "%d posts were successfully marked as draft.",
                updated,
            )
            % updated,
            messages.WARNING,
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

    def display_tags(self, obj):
        """if tags make a flat list of them"""
        tags_list = obj.tags.all().values_list("name", flat=True)
        return ", ".join(tags_list)

    # new feature: adjust admin (see three func below)
    # current admin will be auto-selected in add post view

    def get_readonly_fields(self, request, obj=None):
        """
        prevent more than 1 author choice;
        author field will be current user from request
        """
        if obj is not None:
            return self.readonly_fields + ("author", "letter")
        return self.readonly_fields

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data["author"] = request.user
        data["letter"] = NewsLetter.objects.filter(letter_status=1).last()
        request.GET = data
        return super().add_view(request, form_url="", extra_context=extra_context)

    # new feature: adjust admin (see two func below)
    # using link to access related categ object
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """add current admin kwargs to foreign key fields"""
        if db_field.name == "author":
            kwargs["queryset"] = get_user_model().objects.filter(
                username=request.user.username
            )
        if db_field.name == "letter":
            kwargs["queryset"] = NewsLetter.objects.filter(letter_status=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """remove no value in widget for select fields"""

        if db_field.name == "status":
            select_items = db_field.choices
            kwargs["choices"] = select_items
        if db_field.name == "send_status":
            select_items = db_field.choices
            kwargs["choices"] = select_items
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    @admin_link("categ", _("Категория"))
    def categ_link(self, categ: object):
        return categ

    def get_action_choices(self, request):
        choices = super().get_action_choices(request)
        choices.pop(0)
        return choices
