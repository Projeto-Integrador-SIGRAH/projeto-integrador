from django.urls import reverse
from django.views.generic import TemplateView

from user.permissions import GROUPS_TYPE

from .forms import UserRegistrationForm


class LoginView(TemplateView):
    template_name = "user/login.html"


class CadastroView(TemplateView):
    template_name = "user/cadastro.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserRegistrationForm(group=GROUPS_TYPE.CIDADAO)
        context["api_url"] = reverse("api:register")
        context["login_url"] = reverse("user:login")
        return context


class CadastroAdminView(TemplateView):
    template_name = "user/cadastro_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserRegistrationForm(group=GROUPS_TYPE.ADMIN)
        context["api_url"] = reverse("api:register")
        context["login_url"] = reverse("user:login")
        return context


class PainelView(TemplateView):
    template_name = "user/painel.html"
