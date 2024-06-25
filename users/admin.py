from django.contrib import admin, auth

from .models import AvailableDomain, User

admin.site.unregister(auth.models.Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id", "email")
    search_fields = ("username", "email")
    ordering = ("username",)
    exclude = (
        "groups",
        "password",
        "user_permissions",
    )
    list_filter = ("is_staff", "is_superuser")


@admin.register(AvailableDomain)
class AvailableDomainAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
