from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from src.core.utils.views_help import limit_like
from src.devs.mixins import RestrictHtmxMixin
from src.posts.models.post_model import Post
from src.posts.models.relation_model import Relation

User = get_user_model()


class TrackLike(LRM, RestrictHtmxMixin, View):
    def post(self, request):
        """
        htmx based; create or toggle user likes
        """
        if request.htmx:
            # TODO: log exceeding limit: not fixed catches all calls
            # limit_like(request, attempts=5)
            post_uuid = request.POST.get("post_uuid", None)
            user_id = request.POST.get("user_id", None)
            post = get_object_or_404(Post, uuid=post_uuid)
            user = get_object_or_404(User, id=user_id)
            ctx = {}
            try:
                rel_obj = Relation.objects.get(user=user, post=post)
                rel_obj.like = not bool(rel_obj.like)
                rel_obj.save()
                post.refresh_from_db()
                total_likes = post.count_likes

            except Relation.DoesNotExist:
                Relation.objects.create(user=user, post=post, like=True)
                total_likes = post.count_likes
                ctx.update({"active": True})

            ctx.update({"total_likes": total_likes})

            return render(request, "posts/parts/hart.html", ctx)


class TrackBookmark(LRM, View):
    def post(self, request, *args, **kwargs):
        action = kwargs.get("action")
        msg = None
        try:
            post_uuid = request.POST.get("post_uuid", None)
            user_id = request.POST.get("user_id", None)
            post = get_object_or_404(Post, uuid=post_uuid)
            user = get_object_or_404(User, id=user_id)
            if action == "add":
                obj, created = Relation.objects.get_or_create(
                    user=user, post=post, in_bookmark=True
                )
                msg = "Added to bookmark"
            elif action == "delete":
                rel = get_object_or_404(Relation, user=user, post=post)
                rel.in_bookmark = False
                rel.save()
                msg = "Successfully removed from bookmarks"
            return JsonResponse({"status_code": 200, "msg": msg})
        except Post.DoesNotExist:
            return JsonResponse(
                {"status_code": 404, "msg": "Failed to change bookmark"}
            )
