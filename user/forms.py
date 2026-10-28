from django import forms

from user.permissions import GROUPS_TYPE

INPUT_CLASS = (
    "rounded-lg p-2 border border-sky-400 focus:border-sky-400 "
    "focus:outline-none focus:ring-1 focus:ring-sky-400"
)


class UserRegistrationForm(forms.Form):
    nome = forms.CharField(
        label="Nome completo",
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": INPUT_CLASS, "placeholder": "Nome completo"}
        ),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={"class": INPUT_CLASS, "placeholder": "exemplo@gmail.com"}
        ),
    )
    matricula = forms.CharField(
        label="Matrícula",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": INPUT_CLASS, "placeholder": "Matrícula"}
        ),
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASS, "placeholder": "********"}
        ),
    )
    confirm_password = forms.CharField(
        label="Confirmar senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASS, "placeholder": "********"}
        ),
    )

    def __init__(self, *args, group, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = group
        self.fields["matricula"].required = group == GROUPS_TYPE.ADMIN

        if group == GROUPS_TYPE.CIDADAO:
            self.fields.pop("matricula")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            self.add_error("confirm_password", "As senhas não coincidem.")

        if self.group == GROUPS_TYPE.ADMIN and not cleaned_data.get("matricula"):
            self.add_error(
                "matricula", "A matrícula é obrigatória para administradores."
            )

        return cleaned_data
