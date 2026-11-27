from django.contrib import admin

from .models import Alerta


class AlertaAdmin(admin.ModelAdmin):
    list_display = ("id", "codigo", "reportado_em", "status", "gravidade", "descricao")
    list_filter = ("status", "gravidade")
    search_fields = ("codigo__nome", "descricao")


admin.site.register(Alerta, AlertaAdmin)
