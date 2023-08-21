from django import forms
from django.core import validators
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


class SearchForm(forms.Form):
    """Note: comments preview"""

    q = forms.CharField(
        required=False,
        label="",
        validators=[
            validators.MinLengthValidator(2),
            validators.MaxLengthValidator(250),  # 00),
        ],
        error_messages={"long_query": _("Query is too long")},
    )
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        label=_("This will be treated as spam"),
        validators=[validators.MaxLengthValidator(0)],
        # error_messages={"spam": _("It should not be here")},
    )
    lang = forms.CharField(
        max_length=24,
        required=False,
        widget=forms.HiddenInput,
        label="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        lang = self.fields["lang"]
        lang.initial = get_language()
        search = self.fields["q"]
        search.widget.attrs["class"] = "search-txt"
        search.widget.attrs["placeholder"] = _("Type to search")

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value
