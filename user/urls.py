from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.api.views import UserLoginAPI

from . import views

app_name = "user"

urlpatterns = [
    path("api/login/", UserLoginAPI.as_view(), name="user-login"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("cadastro/", views.CadastroView.as_view(), name="cadastro"),
    path("cadastro_admin/", views.CadastroAdminView.as_view(), name="cadastro_admin"),
    path("painel/", views.PainelView.as_view(), name="painel"),
]
