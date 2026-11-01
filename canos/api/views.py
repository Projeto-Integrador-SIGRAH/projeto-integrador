from api.views import genericModelViewSet
from canos.models import Cano

from .serializers import CanoSerializer


class CanoViewSet(genericModelViewSet):
    # https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    queryset = Cano.objects.all()
    serializer_class = CanoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        # https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself
