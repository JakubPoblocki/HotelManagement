from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import AdminProfile, ClientProfile, ManagerProfile


@admin.register(AdminProfile)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = AdminProfile
    list_display = ("pk", "first_name", "last_name", "email", "is_staff", "is_active",)
    list_display_links = ["pk"]
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        ("Dane personalne", {"fields": ("first_name", "last_name")}),
        (None, {"fields": ("email", "password")}),
        ("Uprawnienia", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    filter_horizontal = ()


@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = ManagerProfile
    list_display = ("pk", "first_name", "last_name", "email", "is_staff", "is_active",)
    list_display_links = ["pk"]
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        ("Dane personalne", {"fields": ("first_name", "last_name")}),
        (None, {"fields": ("email", "password")}),
        ("Uprawnienia", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    filter_horizontal = ()


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = AdminProfile
    list_display = ("pk", "first_name", "last_name", "email", "is_staff", "is_active",)
    list_display_links = ["pk"]
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        ("Dane personalne", {"fields": ("first_name", "last_name")}),
        (None, {"fields": ("email", "password")}),
        ("Uprawnienia", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    filter_horizontal = ()
