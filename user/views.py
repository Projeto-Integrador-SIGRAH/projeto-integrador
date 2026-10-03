from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "user/base_login.html"


class CadastroView(TemplateView):
    template_name = "user/cadastro.html"


class CadastroAdminView(TemplateView):
    template_name = "user/cadastro_admin.html"
