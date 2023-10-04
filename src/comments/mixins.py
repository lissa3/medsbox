from django.core.exceptions import BadRequest
from django.http import HttpResponseForbidden


class CheckRequestMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.htmx:
            raise BadRequest()
        if request.user.banned:
            return HttpResponseForbidden()
        else:
            return super().dispatch(request, *args, **kwargs)
