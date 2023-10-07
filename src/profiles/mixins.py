from django.core.exceptions import BadRequest


class CheckJSMixin:
    """check if request headers present - js fetch"""

    def dispatch(self, request, *args, **kwargs):
        condition = request.headers.get("x-requested-with") == "XMLHttpRequest"
        if request.method == "POST" and not condition:
            raise BadRequest()

        return super().dispatch(request, *args, **kwargs)
