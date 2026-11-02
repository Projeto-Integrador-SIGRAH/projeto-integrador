from django.urls import path

from . import views

app_name = "canos"

urlpatterns = [path("", views.CanosView.as_view(), name="canos")]
