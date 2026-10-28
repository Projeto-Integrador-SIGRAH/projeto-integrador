from django.db import models

class Cano(models.Model):
    class Situacao(models.TextChoices):
        OPERACAO = "OPERACAO", "Em operação"
        MANUTENCAO = "MANUTENCAO", "Manutenção"
        DISPONIVEL = "DISPONIVEL", "Disponível"
        INATIVO = "INATIVO", "Inativo"

    codigo = models.PositiveIntegerField(unique=True)
    diametro = models.PositiveIntegerField()
    material = models.CharField(max_length=50)
    situacao = models.CharField(max_length=15, choices=Situacao, default=Situacao.DISPONIVEL)
    data_instalacao = models.DateField()
    observacao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo

    class Meta:
        ordering = ['-data_instalacao']