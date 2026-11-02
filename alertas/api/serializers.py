from typing import ClassVar

from rest_framework import serializers

from alertas.models import Alerta


class AlertaSerializer(serializers.ModelSerializer):
    codigo = serializers.CharField(source="codigo.codigo", read_only=True)

    class Meta:
        model = Alerta
        fields = "__all__"
        read_only_fields: ClassVar[list[str]] = [
            "reportado_em",
            "tipo",
            "coordenadas",
        ]

    def validate(self, data):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            cano = data.get("codigo")

            alerta_exists = Alerta.objects.filter(
                codigo=cano, codigo__user=request.user, status=Alerta.Status.ENVIADO
            ).exists()

            if alerta_exists:
                raise serializers.ValidationError(
                    "Você não pode criar um novo alerta para este cano enquanto o anterior não for resolvido."
                )

        return data

    # https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
    # https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
