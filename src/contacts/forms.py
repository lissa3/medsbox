from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.conf import settings
from django.core import validators
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        label=_("Your name"),
        validators=[validators.MinLengthValidator(2)],
    )
    subject = forms.CharField(
        max_length=120,
        label=_("Your subject"),
        validators=[validators.MinLengthValidator(2)],
    )
    email = forms.EmailField()
    message = forms.CharField(
        max_length=4000,
        help_text=_("Message field can't be empty"),
        widget=forms.Textarea(attrs={"autocomplete": "email", "rows": 15}),
    )
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    if settings.USE_CAPCHA:
        captcha = ReCaptchaField(
            widget=ReCaptchaV2Checkbox(),
            error_messages={"required": _("You must pass the recapcha test")},
        )

    def clean_message(self):
        message = self.cleaned_data.get("message", "no input")
        words = message.split()
        if len(words) < 2:
            raise forms.ValidationError(
                _("Your message is too short; should contain at least two words")
            )
        return message

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data.get("honeypot")
        if value:
            raise forms.ValidationError(_("It should not be here"))
        return value
