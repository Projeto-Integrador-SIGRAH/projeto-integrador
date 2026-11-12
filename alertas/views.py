from core.views import AuthenticatedView

from .forms import AlertaForm


class ListAlertaView(AuthenticatedView):
    template_name = "alertas/alertas.html"
    form_class = AlertaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alerta_form"] = self.form_class()
        return context
