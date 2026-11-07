from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AuthenticatedView(LoginRequiredMixin, TemplateView):
    pass
