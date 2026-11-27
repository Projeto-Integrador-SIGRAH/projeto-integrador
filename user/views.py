from django.urls import reverse
from core.views import AuthenticatedView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from canos.models import Cano
from user.permissions import GROUPS_TYPE

from .forms import UserLoginForm, UserRegistrationForm


class LoginView(TemplateView):
    template_name = "user/login.html"
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context


class CadastroView(TemplateView):
    template_name = "user/cadastro.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserRegistrationForm(group=GROUPS_TYPE.CIDADAO)
        context["api_url"] = reverse("api:register")
        context["login_url"] = reverse("user:login")
        return context


class CadastroAdminView(TemplateView):
    template_name = "user/cadastro_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserRegistrationForm(group=GROUPS_TYPE.ADMIN)
        context["api_url"] = reverse("api:register")
        context["login_url"] = reverse("user:login")
        return context


class PainelView(PermissionRequiredMixin, AuthenticatedView):
    template_name = "user/painel.html"
    permission_required = "user.can_access_admin_panel"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_canos"] = Cano.objects.count()
        context["canos_em_operacao"] = Cano.objects.filter(
            status=Cano.Status.OPERACAO
        ).count()
        context["canos_em_manutencao"] = Cano.objects.filter(
            status=Cano.Status.MANUTENCAO
        ).count()
        context["canos_disponiveis"] = Cano.objects.filter(
            status=Cano.Status.DISPONIVEL
        ).count()

        context["ultimos_canos"] = Cano.objects.order_by("-criado_em")[:5]

        return context


class AprovacoesView(PermissionRequiredMixin, AuthenticatedView):
    template_name = "user/aprovações.html"
    permission_required = "user.can_access_admin_management"
