from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from src.contacts.exceptions import HtmxFailureError
from src.notifications.models import Notification


@login_required
def get_top_five(request):
    """last five notification: only about replied comments"""
    context = {"top_five": Notification.objects.get_first_five(request.user)}
    return render(request, "notifications/partial.html", context)


@login_required
def make_notifs_read(request):
    """htmx based post request;
    click button in menu drop-down makes all notifications;
    same page displayed
    """
    if request.htmx and request.method == "POST":
        Notification.objects.make_all_read(request.user)
        path_to_go = request.headers["Referer"]
        return HttpResponse(
            headers={
                "HX-Redirect": path_to_go,
            },
        )
    else:
        raise HtmxFailureError(_("Something went wrong.Please try later"))
