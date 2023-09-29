from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin as LRM
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

from .forms import ProfileForm
from .models import Profile


class ProfileView(LRM, View):
    def get(self, request, **kwargs):
        uuid = kwargs.get("uuid")
        profile = get_object_or_404(Profile, uuid=uuid)
        form = ProfileForm(instance=profile)
        ctx = {"profile": profile, "form": form}
        return render(request, "profiles/profile_detail.html", ctx)

    def post(self, request, **kwargs):
        # ajax(fetch) request
        # request.headers.get("x-requested-with") == "XMLHttpRequest")
        uuid = kwargs.get("uuid")
        profile = get_object_or_404(Profile, uuid=uuid)
        form = ProfileForm(request.POST, request.FILES, profile)
        if form.is_valid():
            ava_img = form.cleaned_data.get("avatar")
            if ava_img:
                profile.avatar = ava_img
            else:
                profile.avatar = None
            profile.save()
            return JsonResponse({"status_code": 200, "resp": "OK"})
        else:
            return JsonResponse({"status_code": 404, "err": form.errors})


class ProfileDelete(LRM, View):
    """delete profile"""

    def get(self, request, **kwargs):
        ctx = {}
        uuid = kwargs.get("uuid")
        profile = get_object_or_404(Profile, uuid=uuid, user=request.user)
        ctx = {"profile": profile}
        return render(request, "profiles/profile_delete.html", ctx)

    def post(self, request, **kwargs):
        # TODO implement htmx?
        uuid = kwargs.get("uuid")
        profile = get_object_or_404(Profile, uuid=uuid, user=request.user)
        profile.delete()
        logout(request)
        return redirect("home")
