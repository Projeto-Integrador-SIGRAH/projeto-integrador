from typing import ClassVar

from django import forms
from django.forms import ModelForm

from .models import Alerta


class AlertaForm(ModelForm):
    class Meta:
        model = Alerta
        fields: ClassVar[list[str]] = [
            "codigo",
            "tipo",
            "status",
            "gravidade",
            "coordenadas",
            "descricao",
        ]

    widgets: ClassVar[dict] = {
        "codigo": forms.Select(),
        "status": forms.Select(),
        "gravidade": forms.Select(),
        "descricao": forms.Textarea(
            attrs={
                "placeholder": "Adicione uma descrição detalhada do alerta (entre 20 e 250 caracteres)"
            }
        ),
    }
