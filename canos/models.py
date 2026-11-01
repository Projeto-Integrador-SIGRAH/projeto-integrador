from django.db import models

from user.models import User


class Cano(models.Model):
    class Status(models.TextChoices):
        OPERACAO = "EM_OPERACAO", "Em operação"
        MANUTENCAO = "MANUTENCAO", "Manutenção"
        DISPONIVEL = "DISPONIVEL", "Disponível"
        INATIVO = "INATIVO", "Inativo"

    class Tipo(models.TextChoices):
        AGUA = "Agua", "Água"
        ESGOTO = "Esgoto", "Esgoto"

    codigo = models.CharField(max_length=10, unique=True)
    coordenadas = models.CharField(max_length=50)
    diametro = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=Tipo, default=Tipo.AGUA)
    material = models.CharField(max_length=50)
    status = models.CharField(max_length=15, choices=Status, default=Status.DISPONIVEL)
    responsavel = models.CharField(max_length=100)
    data_instalacao = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    observacao = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.codigo

    class Meta:
        ordering = ["-data_instalacao"]  #  noqa: RUF012
