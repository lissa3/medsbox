from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from src.notifications.models import Notification


@login_required
def get_top_five(request):
    context = {"top_five": Notification.objects.get_first_five(request.user)}
    return render(request, "notifications/partial.html", context)


@login_required
def make_notifs_read(request):
    """htmx post"""
    Notification.objects.make_all_read(request.user)
    return HttpResponseRedirect(request.headers["referer"])
