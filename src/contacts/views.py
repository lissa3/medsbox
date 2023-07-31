from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from src.profiles.models import Profile


class Subscribe(LRM, View):
    def get(self, request):
        """
        only autent-ed users can subscribe to a news letter
        via menu dropdown item
        """
        return render(
            request,
            "contacts/subscription/\
                      confirmation.html",
        )

    def post(self, request, **kwargs):
        """
        htmx_based request with redirect to home page
        and flash msg as a feedback
        """
        try:
            htmx_req = request.headers.get("hx-request")
            if request.user.is_authenticated and htmx_req is not None:
                _id = request.user.profile.id
                profile = get_object_or_404(Profile, id=_id)
                messages.success(request, _("You have subscribed to the news letter"))
                profile.want_news = True
                profile.save()
                return HttpResponse(
                    headers={
                        "HX-Redirect": "/",
                    },
                )
        except Profile.DoesNotExist():
            messages.warning(request, _("Subscription failed"))
            return HttpResponse(
                headers={
                    "HX-Redirect": "/",
                },
            )


class UnSubscribe(View):
    def get(self, request, **kwargs):
        """
        link in newsletter contains profile uuid
        """
        uuid = kwargs.get("uuid")

        profile = get_object_or_404(Profile, uuid=uuid)
        ctx = {"uuid": profile.uuid}
        print("ctx", ctx)
        return render(request, "contacts/subscription/unsubscribe.html", ctx)

    def post(self, request, **kwargs):
        # htmx_based
        try:
            htmx_req = request.headers.get("hx-request")
            uuid = kwargs.get("uuid")
            profile = get_object_or_404(Profile, uuid=uuid)
            if htmx_req and profile:
                messages.success(request, _("You have unsubscribed to the news letter"))
                profile.want_news = False
                profile.save()
                return HttpResponse(
                    headers={
                        "HX-Redirect": "/",
                    },
                )
        except Profile.DoesNotExist():
            messages.warning(request, _("Something went wrong.Subscription failed"))
            return HttpResponse(
                headers={
                    "HX-Redirect": "/",
                },
            )
