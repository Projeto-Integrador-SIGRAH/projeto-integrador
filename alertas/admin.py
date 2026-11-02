from django.contrib import admin

from .models import Alerta

# Register your models here.


@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ("id", "codigo", "tipo", "status", "gravidade", "reportado_em")
    list_filter = ("status", "gravidade", "reportado_em")
    search_fields = ("codigo__nome", "tipo__nome", "descricao")
    ordering = ("-reportado_em",)
    exclude = ("tipo", "coordenadas")
