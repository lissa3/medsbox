from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _

from src.core.utils.views_help import limit_like
from src.posts.models.post_model import Post
from src.posts.models.relation_model import Relation

User = get_user_model()


@login_required
def track_like(request):
    """
    htmx based; create or toggle user likes
    """
    if request.htmx and request.method == "POST":
        post_uuid = request.POST.get("post_uuid", None)
        user_id = request.POST.get("user_id", None)
        post = get_object_or_404(Post, uuid=post_uuid)
        user = get_object_or_404(User, id=user_id)
        ctx = {}
        try:
            if limit_like(request, 5):
                # log user misuses like button
                print("too many attempts to like")
            rel_obj = Relation.objects.get(user=user, post=post)
            # toggle; don't want to use shorthand
            if rel_obj.like:
                rel_obj.like = False
                ctx.update({"active": False})
            else:
                rel_obj.like = True
                ctx.update({"active": True})
            rel_obj.save()
            post.refresh_from_db()
            total_likes = post.count_likes

        except Relation.DoesNotExist:
            Relation.objects.create(user=user, post=post, like=True)
            total_likes = post.count_likes
            ctx.update({"active": True})

        ctx.update({"total_likes": total_likes})

        return render(request, "posts/parts/hart.html", ctx)