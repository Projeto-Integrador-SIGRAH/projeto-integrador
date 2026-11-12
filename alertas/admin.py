from django.contrib import admin

from .models import Alerta

# Register your models here.


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "codigo",
        "tipo",
        "coordenadas",
        "status",
        "gravidade",
        "reportado_em",
    )
    list_filter = ("status", "gravidade", "reportado_em", "tipo")
    search_fields = ("codigo__nome", "tipo__nome", "titulo")
    ordering = ("-reportado_em",)
