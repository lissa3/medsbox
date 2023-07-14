from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """based on AbstractUser model;"""

    search_fields = ("email", "username")
    add_form = UserCreationForm
    list_display = (
        "id",
        "email",
        "last_login",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    readonly_fields = ["last_login", "date_joined"]
    list_filter = ("is_active", "is_superuser")
    add_fieldsets = (
        (
            ("Add Your User"),
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
