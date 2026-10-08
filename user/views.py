from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "user/login.html"


class CadastroView(TemplateView):
    template_name = "user/cadastro.html"


class CadastroAdminView(TemplateView):
    template_name = "user/cadastro_admin.html"


class PainelView(TemplateView):
    template_name = "user/painel.html"


class AprovacoesView(TemplateView):
    template_name = "user/aprovações.html"
