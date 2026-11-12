from rest_framework import serializers

from alertas.models import Alerta
from canos.models import Cano


class AlertaSerializer(serializers.ModelSerializer):
    codigo = serializers.CharField(source="codigo.codigo", read_only=True)
    codigo_id = serializers.PrimaryKeyRelatedField(
        source="codigo",
        queryset=Cano.objects.all(),
        write_only=True,
    )

    # https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield
    class Meta:
        model = Alerta
        fields = "__all__"
        read_only_fields = [  # noqa: RUF012
            "reportado_em",
            "user",
        ]

    def validate(self, data):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            cano = data.get("codigo")

            alerta_exists = Alerta.objects.filter(
                codigo=cano,
                codigo__user=request.user,
                status__in=[Alerta.Status.ENVIADO, Alerta.Status.EM_RESOLUCAO],
            ).exists()

            if alerta_exists:
                raise serializers.ValidationError(
                    "Você não pode criar um novo alerta para este cano enquanto o anterior não for resolvido."
                )

        return data

    # https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation
    # https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
