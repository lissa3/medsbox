from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.http import HttpResponse, JsonResponse
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
            post_uuid = request.POST.get("post_uuid", None)
            user_id = request.POST.get("user_id", None)
            ctx = {}
            try:
                post = get_object_or_404(Post, uuid=post_uuid)
                user = get_object_or_404(User, id=user_id)
                rel_obj = Relation.objects.get(user=user, post=post)
                if rel_obj.like is None:
                    rel_obj.like = True
                else:
                    rel_obj.like = not bool(rel_obj.like)
                ctx.update({"liked": rel_obj.like})
                rel_obj.save()
                post.refresh_from_db()
            except Relation.DoesNotExist:
                # "for the first time create a rel obuj")
                Relation.objects.create(user=user, post=post, like=True)
                ctx.update({"liked": True})

            total_likes = post.count_likes
            ctx.update({"total_likes": total_likes})
            return render(request, "components/relations/liked.html", ctx)


"""
 person_following_list = person.following.values_list('id', flat=True)
        qs = Idea.objects.filter(author_id__in=person_following_list)
"""


class TrackBookmark(LRM, View):
    def post(self, request, *args, **kwargs):
        """
        if user has a part post in bookmarks -> no button `to bookmark` on page;
        otherwise -> click on it-> user flash msg `added` and button gets removed
        via js
        """
        action = kwargs.get("action")
        msg = None
        try:
            post_uuid = request.POST.get("post_uuid", None)
            user_id = request.POST.get("user_id", None)
            post = get_object_or_404(Post, uuid=post_uuid)
            user = get_object_or_404(User, id=user_id)
            print(post, user)
            if action == "add":
                obj, _ = Relation.objects.get_or_create(user=user, post=post)  # noqa
                obj.in_bookmark = True
                obj.save()
                msg = "Added to bookmark"
                return JsonResponse(
                    {"status_code": 200, "msg": msg, "del_button": True}
                )
            elif self.request.htmx and action == "delete":
                # htmx-request for delete
                rel = get_object_or_404(Relation, user=user, post=post)
                rel.in_bookmark = False
                rel.save()
                msg = "Successfully removed from bookmarks"
                # reload: to remove link to bookmaks from menu if no bmark posts
                path_to_go = self.request.headers["Referer"]
                return HttpResponse(
                    status=200,
                    headers={
                        "HX-Redirect": path_to_go,
                    },
                )

        except Post.DoesNotExist:
            if self.request.htmx:
                return HttpResponse(status=404)

            return JsonResponse(
                {"status_code": 404, "msg": "Failed to change bookmark"}
            )
