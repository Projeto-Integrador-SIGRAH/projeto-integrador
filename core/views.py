from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class AuthenticatedView(LoginRequiredMixin, TemplateView):
    pass