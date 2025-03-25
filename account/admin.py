from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser
    list_display = [
        "id",
        "email",
        "username",
    ]


    fieldsets = (
        (None, {"fields": ("phone", "password",)}),
        ("Personal Info", {"fields": ("email", "username", "status",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username","phone", "password1", "password2", "is_superuser","is_active", "is_staff",)}
        ),
    )


