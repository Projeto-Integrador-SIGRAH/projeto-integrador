from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('painel/', views.PainelView.as_view(), name="painel")
]