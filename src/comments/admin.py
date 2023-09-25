from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Comment


@admin.register(Comment)
class CommentAdmin(TreeAdmin):
    form = movenodeform_factory(Comment)
    list_display = [
        "user",
        "post",
        "body",
        "created_at",
        "updated_at",
        "uuid",
        "deleted",
        "reply_to",
    ]
    list_display_links = ["user"]
