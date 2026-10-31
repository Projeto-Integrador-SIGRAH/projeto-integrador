from canos.models import Cano
from .serializers import CanoSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

class CanoViewSet(viewsets.ModelViewSet):
    # https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    queryset = Cano.objects.all()
    serializer_class = CanoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    # https://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        #https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself




