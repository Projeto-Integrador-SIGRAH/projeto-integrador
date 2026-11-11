from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from alertas.models import Alerta
from alertas.permissions import IsOwnerOrReadOnly
from api.views import genericModelViewSet

from .serializers import AlertaSerializer


class AlertaViewSet(genericModelViewSet):
    model = Alerta
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    permission_classes = [  # noqa: RUF012
        IsAuthenticated,
        DjangoModelPermissions,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
