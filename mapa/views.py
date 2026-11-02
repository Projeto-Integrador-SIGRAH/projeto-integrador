from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from canos.forms import CanoForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "mapa/mapa.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CanoForm()
        return context
