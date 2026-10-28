from django.contrib import admin
from .models import Cano

@admin.register(Cano)
class CanoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'localizacao' ,'material', 'situacao', 'responsavel']
    list_filter = ['codigo', 'material', 'situacao']
    search_fields = ['codigo']
    
