from django.contrib import admin

from .models import Cano


@admin.register(Cano)
class CanoAdmin(admin.ModelAdmin):
    list_display = ["codigo", "material", "status", "responsavel"]  # noqa: RUF012
    list_filter = ["codigo", "material", "status"]  # noqa: RUF012
    search_fields = ["codigo"]  # noqa: RUF012
