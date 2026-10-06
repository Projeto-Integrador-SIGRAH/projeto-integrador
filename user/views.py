from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "user/login.html"


class PainelView(TemplateView):
    template_name = "user/painel.html"
