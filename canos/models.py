from django.db import models

class Cano(models.Model):
    class Situacao(models.TextChoices):
        OPERACAO = "OPERACAO", "Em operação"
        MANUTENCAO = "MANUTENCAO", "Manutenção"
        DISPONIVEL = "DISPONIVEL", "Disponível"
        INATIVO = "INATIVO", "Inativo"

    codigo = models.CharField(max_length=10, unique=True)
    localizacao = models.CharField(max_length=150)
    coordenadas = models.CharField(max_length=50)
    diametro = models.PositiveIntegerField()
    material = models.CharField(max_length=50)
    situacao = models.CharField(max_length=15, choices=Situacao, default=Situacao.DISPONIVEL)
    responsavel = models.CharField(max_length=100)
    data_instalacao = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.codigo

    class Meta:
        ordering = ['-data_instalacao']