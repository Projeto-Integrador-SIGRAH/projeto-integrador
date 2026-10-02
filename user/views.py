from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = "user/base_login.html"

class AprovacoesView(TemplateView):
    template_name = "user/aprovações.html"
