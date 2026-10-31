from django.views.generic import TemplateView
from django.urls import reverse
from .forms import CanoForm

class CanosView(TemplateView):
    template_name = "canos/canos.html"
    form_class = CanoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CanoForm()
        return context

