from django.utils import timezone
from rest_framework import serializers

from canos.models import Cano


class CanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cano
        fields = [  # noqa: RUF012
            "id",
            "codigo",
            "coordenadas",
            "diametro",
            "tipo",
            "material",
            "status",
            "equipe_responsavel",
            "data_instalacao",
            "criado_em",
            "atualizado_em",
            "observacoes",
            "user",
        ]
        read_only_fields = [  # noqa: RUF012
            "id",
            "criado_em",
            "atualizado_em",
            "user",
        ]
        # https://www.django-rest-framework.org/api-guide/serializers/#specifying-fields-explicitly

    def validate_codigo(self, value):
        if Cano.objects.filter(codigo__iexact=value).exists() and self.instance is None:
            raise serializers.ValidationError("Já existe um cano com esse código.")
        return value

    def validate_data_instalacao(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError(
                "A data de instalação não pode ser futura"
            )
        return value
