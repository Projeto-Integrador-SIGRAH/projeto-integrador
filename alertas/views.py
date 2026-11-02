from core.views import AuthenticatedView

class ListAlertaView(AuthenticatedView):
    template_name = "alertas/alertas.html"
