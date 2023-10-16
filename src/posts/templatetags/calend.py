from datetime import datetime

from django import template
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.posts.models.post_model import Post

register = template.Library()

month_collection = [
    (1, _("January")),
    (2, _("February")),
    (3, _("March")),
    (4, _("April")),
    (5, _("May")),
    (6, _("June")),
    (7, _("July")),
    (8, _("August")),
    (9, _("September")),
    (10, _("October")),
    (11, _("November")),
    (12, _("December")),
]


@register.inclusion_tag("components/calend.html")
def calend_posts(**kwargs):
    """substitute template sidebar `calender` public posts
    in form of tuple(month-number,month-str,count posts for the date)
    """
    _date = datetime.now()
    current_year = int(_date.strftime("%Y"))
    start = datetime(2023, 1, 1)
    tz_start = timezone.make_aware(start)
    end = datetime(2023, 12, 31)
    tz_end = timezone.make_aware(end)
    posts = (
        Post.objects.get_public()
        .values("published_at")
        .filter(published_at__range=[tz_start, tz_end])
    )

    res = []
    for month in month_collection:
        _count = posts.filter(published_at__month=month[0]).count()
        if _count:
            res.append((month[0], month[1], _count))

    return {"year": current_year, "res": res}
