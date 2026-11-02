from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated


class genericModelViewSet(viewsets.ModelViewSet):
    # https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    permission_classes = [IsAuthenticated, DjangoModelPermissions]  #  noqa: RUF012
