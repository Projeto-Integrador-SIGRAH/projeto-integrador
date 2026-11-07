from django import forms
from django.forms import ModelForm

from .models import Alerta


class AlertaForm(ModelForm):
    class Meta:
        model = Alerta
        fields = [  # noqa: RUF012
            "codigo",
            "status",
            "gravidade",
            "titulo",
            "tipo",
            "descricao",
        ]

        widgets = {  # noqa: RUF012
            "codigo": forms.Select(),
            "status": forms.Select(),
            "gravidade": forms.Select(),
            "titulo": forms.TextInput(
                attrs={"placeholder": "Adicione um título para o alerta"}
            ),
            "tipo": forms.Select(),
            "descricao": forms.Textarea(
                attrs={
                    "placeholder": "Adicione uma descrição detalhada do alerta (entre 20 e 250 caracteres)"
                }
            ),
        }
