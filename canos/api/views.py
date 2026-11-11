from rest_framework.exceptions import ValidationError

from api.views import genericModelViewSet
from canos.models import Cano

from .serializers import CanoSerializer


class CanoViewSet(genericModelViewSet):
    # https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    queryset = Cano.objects.all()
    serializer_class = CanoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        codigo = params.get("codigo")
        material = params.get("material")
        status = params.get("status")
        diametro = params.get("diametro")

        if codigo:
            queryset = queryset.filter(codigo__iexact=codigo)
        if material:
            queryset = queryset.filter(material__iexact=material)
        if status:
            queryset = queryset.filter(status=status)
        if diametro:
            try:
                diametro = int(diametro)
            except ValueError as error:
                raise ValidationError(
                    {"diametro": "Informe um diâmetro válido."}
                ) from error
            queryset = queryset.filter(diametro=diametro)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        # https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself
