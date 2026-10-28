from django.contrib import admin
from .models import Cano

@admin.register()
class CanoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'material', 'situacao']
    list_filter = ['codigo', 'material']
    search_fields = ['codigo']
    
