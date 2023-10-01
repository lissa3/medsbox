from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as UCF
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserCreationForm(UCF):
    """form to create a new user via admin (door admin)"""

    email = forms.EmailField(
        label=_("Email"),
        max_length=120,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    class Meta(UCF.Meta):
        model = User
        fields = ("username", "email")


# custom allauth form
class CustomSignupForm(SignupForm):
    """add extra field for 'Agree'"""

    username_help_text = "Username should contain at least 3 characters"
    password_help_text = (
        "Password should contain at least 8 characters; can not be entirely numeric"
    )

    def __init__(self, *args, **kwargs):
        """included field "agree to term" needs other css styling"""
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = self.username_help_text
        self.fields["password1"].help_text = self.password_help_text

        self.fields["agree_to_terms"].widget.attrs = {"type": "checkbox"}
        for field_name, field in self.fields.items():
            if field_name != "agree_to_terms":
                field.widget.attrs = {"class": "form-control border border-4"}
            else:
                field.widget.attrs = {"class": "mt-2 mb-4"}

    agree_to_terms = forms.BooleanField(
        label=format_html(
            _(
                "I agree to the <a class='general' \
                href='/terms'>terms and conditions</a>"
            )
        )
    )
    field_order = ("username", "email", "password1", "password2", "agree_to_terms")
