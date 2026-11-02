from core.views import AuthenticatedView

from canos.forms import CanoForm


class IndexView(AuthenticatedView):
    template_name = "mapa/mapa.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CanoForm()
        return context
