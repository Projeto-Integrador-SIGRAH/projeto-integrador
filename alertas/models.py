from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from canos.models import Cano


# Create your models here.
class Alerta(models.Model):
    class Status(models.TextChoices):
        ENVIADO = "ENVIADO", "Enviado"
        EM_RESOLUCAO = "EM_RESOLUCAO", "Em resolução"
        RESOLVIDO = "RESOLVIDO", "Resolvido"

    class Gravidade(models.TextChoices):
        BAIXA = "3_Baixa", "Baixa"
        MEDIA = "2_Media", "Média"
        ALTA = "1_Alta", "Alta"

    class Tipo(models.TextChoices):
        ENTUPIMENTO = "ENTUPIMENTO", "Entupimento"
        VAZAMENTO = "VAZAMENTO", "Vazamento"
        OBSTRUCAO = "OBSTRUCAO", "Obstrução"
        OUTRO = "OUTRO", "Outro"

    codigo = models.ForeignKey(
        Cano, on_delete=models.PROTECT, related_name="alertas_codigo"
    )
    coordenadas = models.CharField(max_length=50, blank=True)
    reportado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.ENVIADO
    )
    gravidade = models.CharField(
        max_length=10, choices=Gravidade.choices, default=Gravidade.ALTA
    )
    titulo = models.CharField(max_length=100, blank=True)
    tipo = models.CharField(
        max_length=15, choices=Tipo.choices, default=Tipo.ENTUPIMENTO
    )
    descricao = models.TextField(
        validators=[
            MinLengthValidator(
                20, message="A descrição deve ter pelo menos 20 caracteres."
            ),
            MaxLengthValidator(
                250, message="A descrição não pode passar de 250 caracteres."
            ),
        ]
    )
    # https://docs.djangoproject.com/en/6.1/ref/validators/

    def __str__(self):
        return f"Alerta {self.id} - {self.status}"

    class Meta:
        ordering = ["gravidade", "-reportado_em", "tipo"]  #  noqa: RUF012
