from django.contrib import admin

<<<<<<< HEAD
from .models import Cano
=======
from .models import Cano, Equipe, Material


@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ["nome"]  # noqa: RUF012


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ["tipo"]  # noqa: RUF012

>>>>>>> 116acc3 (add listagem with details)


@admin.register(Cano)
class CanoAdmin(admin.ModelAdmin):
    list_display = ["codigo", "material", "status", "equipe_responsavel"]  # noqa: RUF012
    list_filter = ["codigo", "material", "status"]  # noqa: RUF012
    search_fields = ["codigo"]  # noqa: RUF012
