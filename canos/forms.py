from django import forms
from django.forms import ModelForm

from .models import Cano


class CanoForm(ModelForm):
    class Meta:
        model = Cano
        fields = [  # noqa: RUF012
            "codigo",
            "coordenadas",
            "diametro",
            "tipo",
            "material",
            "status",
            "responsavel",
            "data_instalacao",
            "observacao",
        ]
        widgets = {  # noqa: RUF012
            "codigo": forms.TextInput(attrs={"placeholder": "Ex.: A-0002"}),
            "coordenadas": forms.TextInput(
                attrs={"placeholder": "Ex.: -6.0965, -38.2065"}
            ),
            "diametro": forms.NumberInput(
                attrs={"placeholder": "Informe o diâmetro em mm"}
            ),
            "tipo": forms.Select(),
            "material": forms.TextInput(
                attrs={"placeholder": "Informe o material do cano"}
            ),
            "status": forms.Select(),
            "responsavel": forms.TextInput(
                attrs={"placeholder": "Informe o responsável pelo cano"}
            ),
            "data_instalacao": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
            "observacao": forms.Textarea(
                attrs={"placeholder": "Adicione observações sobre o cano"}
            ),
        }
