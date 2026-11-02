from django.urls import path

from . import views

app_name = "alertas"

urlpatterns = [path("", views.AlertaView.as_view(), name="alertas")]
