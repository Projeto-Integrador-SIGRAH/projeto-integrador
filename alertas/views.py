from django.views.generic import TemplateView

from .forms import AlertaForm


class AlertaView(TemplateView):
    template_name = "alertas/alertas.html"
    form_class = AlertaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context
