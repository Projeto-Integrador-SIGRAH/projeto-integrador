from django.db import models

from user.models import User


class Equipe(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Material(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name_plural = "Materiais"


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
    coordenadas = models.TextField()
    diametro = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=Tipo, default=Tipo.AGUA)
    material = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=15, choices=Status, default=Status.DISPONIVEL)
    equipe_responsavel = models.ForeignKey(
        Equipe, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    data_instalacao = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    observacoes = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.codigo

    class Meta:
        ordering = ["-data_instalacao"]  #  noqa: RUF012
