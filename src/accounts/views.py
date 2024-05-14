from allauth.account.views import SignupView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render

User = get_user_model()


class CustomSignUp(SignupView):
    """if user deleted his account=> show account not active template"""

    def form_valid(self, form):
        user_email = form.cleaned_data["email"]
        user_obj = get_object_or_404(User, email=user_email)
        if user_obj is not None and not user_obj.is_active:
            return render(self.request, template_name="account/account_inactive.html")
        print("inside line 14")
        return super().form_valid(form)
