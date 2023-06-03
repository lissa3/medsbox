from allauth.account.adapter import DefaultAccountAdapter
from django.utils.translation import gettext_lazy as _


class InactiveUserEmailAdapter(DefaultAccountAdapter):
    """
    adjusting registration flow: make "email_taken" more
    generic allauth:
    email_taken": _("A user is already  registered with this
    e-mail address."),
    (user deactivated his account in the past and  tries to
    create it again
    """

    error_messages = DefaultAccountAdapter.error_messages
    update_email_err_msg = {
        "email_taken": _(
            "Can not create an account with this e-mail  \
            address or use another one. Please contact the admin"
        )
    }
    error_messages.update(update_email_err_msg)
