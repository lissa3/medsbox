from django.contrib.auth import get_user_model
from django.db import models

from src.posts.models.post_model import Post

User = get_user_model()


class Relation(models.Model):
    """if attr  like get updated -> cached fields in post model will be also re-calculated"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rel")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_rel")
    like = models.BooleanField(blank=True, default=False)
    in_bookmark = models.BooleanField(blank=True, default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_bmarks = self.in_bookmark
        self.old_like = self.like

    def save(self, *args, **kwargs):
        from src.core.utils.model_help import calc_count_likes, calc_count_marks

        # if like changed |=> re-calc total likes on post
        start_creating = not self.pk
        super().save(*args, **kwargs)

        new_like = self.like
        new_bmark = self.in_bookmark

        if self.old_like != new_like or start_creating:
            # user-post-rel obj is just created
            calc_count_likes(self.post)
        if self.old_bmarks != new_bmark or start_creating:
            calc_count_marks(self.post)

    def __str__(self):
        return f"User: {self.user} active in user-post-relations {self.like}"
