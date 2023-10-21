from django.core.exceptions import BadRequest, PermissionDenied
from django.shortcuts import get_object_or_404

from src.posts.models.post_model import Post


class StaffUserRequiredMixin:
    """Verify that the current user is authenticated AND user is_staff."""

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_staff):
            raise PermissionDenied("You do not have enough permission to see this page")
        return super().dispatch(request, *args, **kwargs)


class RestricToAuthorMixin:
    """restrict access to dev post changes only to the author or superuser"""

    def get_object(self):
        uuid = self.kwargs.get("uuid")
        obj = get_object_or_404(Post, uuid=uuid)
        if self.request.user == obj.author or self.request.user.is_superuser:
            pass
        else:
            raise PermissionDenied("You do not have enough permission to see this page")

        return obj


class RestrictHtmxMixin:
    """
    Only htmx allowed
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.htmx:
            raise BadRequest("only htmx allowed")
        return super().dispatch(request, *args, **kwargs)
