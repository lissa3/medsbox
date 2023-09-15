from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from src.comments.models import Comment

User = get_user_model()


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        max_length=4000,
        help_text=_("Comment can't be empty"),
        widget=forms.Textarea(attrs={"rows": 15}),
    )
    comm_parent_id = forms.IntegerField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Comment
        fields = ["body"]
