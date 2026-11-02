from typing import ClassVar

from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from alertas.models import Alerta
from api.views import genericModelViewSet

from .serializers import AlertaSerializer


class AlertaViewSet(genericModelViewSet):
    model = Alerta
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    permission_classes: ClassVar[list] = [
        IsAuthenticated,
        DjangoModelPermissions,
    ]
