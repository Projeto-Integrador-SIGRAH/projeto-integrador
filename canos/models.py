from django.db import models

class Cano(models.Model):
    class Situacao(models.TextChoices):
        OPERACAO = "OPERACAO", "Em operação"
        MANUTENCAO = "MANUTENCAO", "Manutenção"
        DISPONIVEL = "DISPONIVEL", "Disponível"
        INATIVO = "INATIVO", "Inativo"

    codigo = models.PositiveIntegerField(unique=True)
    localizacao = models.CharField(max_length=150)
    coordenadas = models.CharField(max_length=50)
    diametro = models.PositiveIntegerField()
    material = models.CharField(max_length=50)
    situacao = models.CharField(max_length=15, choices=Situacao, default=Situacao.DISPONIVEL)
    responsavel = models.CharField(max_length=100)
    data_instalacao = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.atualizado_em = timezone.now()

        super().save(*args, **kwargs)
    # docs.djangoproject.com/en/6.1/topics/db/models/#overriding-predefined-model-methods

    def __str__(self):
        return self.codigo

    class Meta:
        ordering = ['-data_instalacao']