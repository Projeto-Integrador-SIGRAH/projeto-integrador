from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("cadastro/", views.CadastroView.as_view(), name="cadastro"),
    path("cadastro_admin/", views.CadastroAdminView.as_view(), name="cadastro_admin"),
]
