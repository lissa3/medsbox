import logging

from django.core.exceptions import BadRequest

from src.core.utils.views_help import get_ip

logger = logging.getLogger("django")


class CheckJSMixin:
    """check if request headers present - js fetch"""

    def dispatch(self, request, *args, **kwargs):
        condition = request.headers.get("x-requested-with") == "XMLHttpRequest"
        if request.method == "POST" and not condition:
            remote_address = get_ip(request)
            logger.warning(f"request attempt not htmx from ip: {remote_address}")
            raise BadRequest()

        return super().dispatch(request, *args, **kwargs)
