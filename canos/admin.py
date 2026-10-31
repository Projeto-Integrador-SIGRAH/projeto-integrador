from django.contrib import admin
from .models import Cano

@admin.register(Cano)
class CanoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'localizacao' ,'material', 'status', 'responsavel']
    list_filter = ['codigo', 'material', 'status']
    search_fields = ['codigo']
    
