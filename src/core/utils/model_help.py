from django.db.models import Case, Count, When

from src.posts.models.relation_model import Relation


def calc_count_likes(obj):
    agr_likes = Relation.objects.filter(post=obj).aggregate(
        total_likes=(Count(Case(When(like=True, then=1))))
    )
    obj.count_likes = agr_likes.get("total_likes", None)
    obj.save()
