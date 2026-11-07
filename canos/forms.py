from django import forms
from django.forms import ModelForm

from .models import Cano

INPUT_CLASS = "rounded-lg p-2 border border-gray-400 focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"


class CanoForm(ModelForm):
    class Meta:
        model = Cano
        fields = [  # noqa: RUF012
            "codigo",
            "diametro",
            "tipo",
            "material",
            "status",
            "equipe_responsavel",
            "data_instalacao",
            "observacoes",
        ]
        widgets = {  # noqa: RUF012
            "codigo": forms.TextInput(
                attrs={"placeholder": "Ex.: A-0002", "class": INPUT_CLASS}
            ),
            "diametro": forms.NumberInput(
                attrs={"placeholder": "Informe o diâmetro em mm", "class": INPUT_CLASS}
            ),
            "tipo": forms.Select(attrs={"class": INPUT_CLASS, "label": "Tipo do cano"}),
            "material": forms.TextInput(
                attrs={
                    "placeholder": "Informe o material do cano",
                    "class": INPUT_CLASS,
                }
            ),
            "status": forms.Select(attrs={"class": INPUT_CLASS}),
            "equipe_responsavel": forms.TextInput(
                attrs={
                    "placeholder": "Informe o responsável pelo cano",
                    "class": INPUT_CLASS,
                }
            ),
            "data_instalacao": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date", "class": INPUT_CLASS},
            ),
            "observacao": forms.Textarea(
                attrs={
                    "placeholder": "Adicione observações sobre o cano",
                    "class": INPUT_CLASS,
                    "rows": 2,
                }
            ),
        }
