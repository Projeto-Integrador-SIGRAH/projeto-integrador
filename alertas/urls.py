from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListAlertaView.as_view(), name="alertas")
]