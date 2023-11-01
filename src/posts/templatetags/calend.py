from datetime import date

from django import template
from django.utils.translation import gettext_lazy as _

from src.posts.models.post_model import Post

register = template.Library()


@register.inclusion_tag("posts/parts/archive.html")
def show_archive(**kwargs):
    """substitute template sidebar `calender` with dropdown archive"""
    arch = Post.objects.get_public().datetimes("published_at", "month", order="DESC")
    # print("arch is", arch.count()) # amount months with posts
    archives = {}
    for item in arch:
        year = item.year
        month = item.month
        print("month ", month)
        for i in range(1, 13):
            if i == month:
                try:
                    archives[year].append(
                        (
                            date(year, month, 1),
                            Post.objects.get_public()
                            .filter(published_at__month=month, published_at__year=year)
                            .count(),
                        )
                    )
                except KeyError:
                    archives[year] = [
                        (
                            date(year, month, 1),
                            Post.objects.get_public()
                            .filter(published_at__month=month, published_at__year=year)
                            .count(),
                        )
                    ]
    sorted_final = sorted(archives.items(), reverse=True)

    return {"archives": sorted_final}
