from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "mapa/mapa.html"

    def get_login_url(self):
        return reverse("user:login")
