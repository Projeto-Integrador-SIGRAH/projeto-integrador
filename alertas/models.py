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

    codigo = models.ForeignKey(
        Cano, on_delete=models.PROTECT, related_name="alertas_codigo"
    )
    reportado_em = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=Cano.Tipo.choices, blank=True)
    status = models.CharField(max_length=15, choices=Status, default=Status.ENVIADO)
    gravidade = models.CharField(
        max_length=10, choices=Gravidade, default=Gravidade.ALTA
    )
    coordenadas = models.CharField(max_length=50, blank=True)
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

    def save(self, *args, **kwargs):
        if self.codigo:
            self.tipo = self.codigo.tipo
            self.coordenadas = self.codigo.coordenadas
        super().save(*args, **kwargs)

    # https://docs.djangoproject.com/en/6.1/topics/db/models/
    class Meta:
        ordering = ["gravidade", "-reportado_em"]  #  noqa: RUF012
