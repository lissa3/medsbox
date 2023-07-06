from django.contrib import admin
from django.db.models import Count, DateTimeField, Max, Min
from django.db.models.functions import Trunc
from django.urls import reverse

from .models import Profile, ProfileChart


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """display courses in charts on change_list"""

    list_display = (
        "id",
        "created_at",
        "user",
        "avatar",
        "info",
    )
    list_filter = ("created_at", "user")
    list_display_links = ["user"]
    date_hierarchy = "created_at"


def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + "__day" in request.GET:
        return "hour"
    if date_hierarchy + "__month" in request.GET:
        return "day"
    if date_hierarchy + "__year" in request.GET:
        return "week"
    return "month"


@admin.register(ProfileChart)
class ProfileChartAdmin(admin.ModelAdmin):
    """ProfileChart is proxy model Profile;
    parse GET req querystring to get it a given period of time;
    and show profiles per that period;
    see css changelist bar-chart (line 331-385)
    """

    change_list_template = "profiles/admin/chart_change_list.html"
    date_hierarchy = "created_at"

    def changelist_view(self, request, extra_context=None):
        # total ({'total': 32}), period, per_day
        response = super().changelist_view(request, extra_context=extra_context)
        period = get_next_in_date_hierarchy(request, self.date_hierarchy)

        response.context_data["period"] = period
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response
        # list view
        metrics = {"total": Count("id")}
        total_num = dict(qs.aggregate(**metrics))
        response.context_data["total"] = total_num
        total = total_num["total"]  # 7
        print("total is ", total)
        calc_qs = (
            qs.annotate(
                period=Trunc("created_at", "day", output_field=DateTimeField()),
            )
            .values("period")
            .annotate(sub_total=Count("id"))
            .order_by("period")
        )

        summary = []
        for list_item in calc_qs:
            percent = round(list_item["sub_total"] * 100 / total)
            list_item["sub_percent"] = percent
            summary.append(list_item)

        response.context_data["summary"] = summary

        summary_range = calc_qs.aggregate(
            low=Min("sub_total"),
            high=Max("sub_total"),
        )
        high = summary_range.get("high", 0)
        low = summary_range.get("low", 0)
        response.context_data["sum_over_time"] = [
            {
                "period": x["period"],
                "sub_total": x["sub_total"] or 0,
                "pct": ((x["sub_total"] or 0) - low) / (high - low) * 100
                if high > low
                else 0,
            }
            for x in calc_qs
        ]
        # above if event one time |=> high - low = 0|=> zero divvisionError
        # print(response.context_data["sum_over_time"])
        # sum_over_time = [
        # {period': datetime.date(2023, 4, 8), 'sub_total': 10, 'pct': 90.0},...
        # ]

        return response
