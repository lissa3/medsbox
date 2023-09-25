from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from src.comments.forms import CommentForm
from src.comments.models import Comment
from src.notifications.models import Notification
from src.posts.models.post_model import Post


def display_all_comments(request, post_uuid):
    post = Post.objects.get(uuid=post_uuid)
    post_comms = Comment.objects.filter(post=post)
    return render(
        request,
        "components/comms/wraps.html",
        {"comments": post_comms, "post": post, "user": request.user},
    )


@login_required
def get_reply_form(request, post_uuid, comm_id):
    """get req to get form for reply"""
    form = CommentForm(initial={"comm_parent_id": comm_id})
    ctx = {}
    ctx["form"] = form
    ctx["post_uuid"] = post_uuid
    return render(request, "components/comms/comm_form.html", ctx)


@require_http_methods(["POST"])
@login_required
def process_reply(request, post_uuid):
    """
    if parent comm is deleted->no notifications;
    also no notif users own comment
    """
    form = CommentForm(request.POST)
    if form.is_valid():
        comm_parent_id = form.cleaned_data["comm_parent_id"]
        post = get_object_or_404(Post, uuid=post_uuid)
        parent_comm = get_object_or_404(Comment, id=comm_parent_id)
        replied_to = parent_comm.user
        comm = form.save(commit=False)
        comm_body = form.cleaned_data["body"]
        comm.user = request.user
        comm.reply_to = replied_to
        comm.post = post
        comm.body = comm_body
        if replied_to == request.user:
            comm.own_reply = True
        parent_comm.add_child(instance=comm)
        return HttpResponse(status=204, headers={"HX-Trigger": "updateCommList"})


@login_required
def handle_edit_comment(request, post_uuid, comm_id):
    """htmx based + modal UI in bootstrap5"""

    ctx = {"post_uuid": post_uuid, "comm_id": comm_id}
    post = get_object_or_404(Post, uuid=post_uuid)
    obj = get_object_or_404(Comment, post_id=post.id, id=comm_id)
    parent = obj.get_parent()
    if request.method == "GET":
        if parent:
            form = CommentForm(instance=obj, initial={"comm_parent_id": comm_id})

        else:
            print("should be a root comment")
            form = CommentForm(instance=obj)
        ctx["form"] = form
        return render(request, "components/comms/comm_edit_form.html", ctx)

    if request.method == "PUT":
        data_dict = QueryDict(request.body).dict()

        form = CommentForm(data_dict, instance=obj)
        if form.is_valid():
            print("cleaned data reply is ", form.cleaned_data)
            obj.updated_at = timezone.now()
            obj.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "updateCommList"})
        else:
            print("form NOT valid")
            print("errs: ", form.errors)
            ctx["fomr"] = form
    return render(request, "components/comms/comm_edit_form.html", ctx)


@login_required
def handle_delete_comment(request, post_uuid, comm_id):
    """htmx based"""
    ctx = {"post_uuid": post_uuid, "comm_id": comm_id}
    post = get_object_or_404(Post, uuid=post_uuid)
    comm_to_del = get_object_or_404(Comment, id=comm_id, post_id=post.id)
    if request.method == "GET":
        return render(request, "components/comms/del_confirm.html", ctx)
    else:
        comm_to_del.deleted = True
        comm_to_del.save()
        print("Comm deleted successfully!")
        return HttpResponse(status=204, headers={"HX-Trigger": "updateCommList"})
