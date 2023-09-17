from django.urls import path

from .views import (
    display_all_comments,
    get_reply_form,
    handle_delete_comment,
    handle_edit_comment,
    process_reply,
)

app_name = "comments"

urlpatterns = [
    path("all-comms/<post_uuid>/", display_all_comments, name="all_comms"),
    # create
    path("add-comm/<post_uuid>/<comm_id>/", get_reply_form, name="add_comm"),
    path("process-reply/<post_uuid>/", process_reply, name="process_comm"),
    # delete
    path(
        "process-delete/<post_uuid>/<comm_id>/",
        handle_delete_comment,
        name="handle_delete",
    ),
    # edit
    path("edit-comm/<post_uuid>/<comm_id>/", handle_edit_comment, name="handle_edit"),
]
