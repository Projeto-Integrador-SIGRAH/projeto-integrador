from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "nome", "get_groups", "is_staff")
    search_fields = ("email", "nome", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")


admin.site.register(User, UserAdmin)
