from django.db import models
from django.contrib.auth.models import User

class Linha(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class Ponto(models.Model):
    nome = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    linha = models.ForeignKey(Linha, on_delete=models.CASCADE, related_name="pontos")

    def __str__(self):
        return f"{self.nome} ({self.linha.codigo})"

class Motorista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True)
    status = models.CharField(max_length=30, default="disponível")
    linha_atual = models.ForeignKey(Linha, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Localizacao(models.Model):
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE, related_name="localizacoes")
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.motorista.user.username} @ {self.timestamp.strftime('%H:%M:%S')}"
