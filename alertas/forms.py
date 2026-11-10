from django import forms
from django.forms import ModelForm

from .models import Alerta

INPUT_CLASS = "rounded-lg p-2 border border-gray-400 focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"


class AlertaForm(ModelForm):
    class Meta:
        model = Alerta
        fields = [  # noqa: RUF012
            "gravidade",
            "titulo",
            "tipo",
            "descricao",
        ]

        widgets = {  # noqa: RUF012
            "titulo": forms.TextInput(
                attrs={
                    "placeholder": "Adicione um título para o alerta",
                    "class": INPUT_CLASS,
                }
            ),
            "tipo": forms.Select(
                attrs={"label": "Tipo do alerta", "class": INPUT_CLASS}
            ),
            "gravidade": forms.Select(
                attrs={"label": "Gravidade do alerta", "class": INPUT_CLASS}
            ),
            "descricao": forms.Textarea(
                attrs={
                    "placeholder": "Adicione uma descrição detalhada do alerta (entre 20 e 250 caracteres)",
                    "class": INPUT_CLASS,
                }
            ),
        }
