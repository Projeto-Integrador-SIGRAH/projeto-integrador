from alertas.forms import AlertaForm
from core.views import AuthenticatedView

from .forms import CanoForm


class CanosView(AuthenticatedView):
    template_name = "canos/canos.html"
    form_class = CanoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CanoForm()
        context["alerta_form"] = AlertaForm()
        return context
