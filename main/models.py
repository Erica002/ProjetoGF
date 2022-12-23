from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

RENDA_CHOICES = [
    ("Salário", "Salário"),
    ("Freelancer", "Freelancer"),
    ("Extra", "Extra"),
]

CLASSES_CHOICES = [
    ("Cartão de Crédito", "Cartão de Crédito"),
    ("Dinheiro", "Dinheiro"),
    ("Pix", "Pix"),
]


class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    usuario = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Despesa(models.Model):
    detalhes = models.TextField()
    valor_despesa = models.FloatField()
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    forma_pagamento = models.CharField(
        default="Dinheiro", max_length=155, choices=CLASSES_CHOICES
    )
    usuario = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.detalhes


class Renda(models.Model):
    detalhes = models.CharField(max_length=255)
    valor_renda = models.FloatField()
    origem = models.CharField(default="Extra", max_length=155, choices=RENDA_CHOICES)
    data = models.DateField(default=now)
    usuario = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.detalhes


class Wishlist(models.Model):
    detalhes = models.CharField(max_length=255)
    valor_necessario = models.FloatField()
    valor_salvo = models.FloatField(default=0)
    data = models.DateField(default=now)
    usuario = models.ForeignKey(to=User, on_delete=models.CASCADE)
