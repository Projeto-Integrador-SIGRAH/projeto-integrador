from django.shortcuts import render
from django.views.generic import TemplateView

class ListAlertaView(TemplateView):
    template_name = 'alertas/alertas.html'

