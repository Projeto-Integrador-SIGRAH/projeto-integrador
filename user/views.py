from django.views.generic import TemplateView

from .forms import UserLoginForm


class LoginView(TemplateView):
    template_name = "user/login.html"
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context


class CadastroView(TemplateView):
    template_name = "user/cadastro.html"


class CadastroAdminView(TemplateView):
    template_name = "user/cadastro_admin.html"


class PainelView(TemplateView):
    template_name = "user/painel.html"
