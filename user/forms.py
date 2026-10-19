from django import forms

INPUT_CLASS = "rounded-lg p-2 border border-sky-400 focus:border-sky-400 focus:outline-none focus:ring-1 focus:ring-sky-400"


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={"class": INPUT_CLASS, "placeholder": "exemplo@gmail.com"}
        ),
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": INPUT_CLASS, "placeholder": "********"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            raise forms.ValidationError("Email e senha são obrigatórios.")

        return cleaned_data
