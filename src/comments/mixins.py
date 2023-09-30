from django.http import HttpResponseForbidden


class CheckBannedMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.banned:
            return HttpResponseForbidden()
        else:
            return super().dispatch(request, *args, **kwargs)
