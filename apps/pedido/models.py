from django.db import models
from django.contrib.auth.models import User
from apps.cardapio.models import ItemCardapio

# Create your models here.
class FormaPagamento(models.Model):
    situacao = models.BooleanField(default=False)
    descricao = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.descricao

class StatusPedido(models.Model):
    situacao = models.BooleanField(default=False)
    descricao = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.descricao
    
class Pedido(models.Model):
    numero_mesa = models.IntegerField(null=False)
    valor_total = models.FloatField(null=False, blank=False, default=0.0)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.SET_NULL, null=True, blank=True, default="")
    status = models.ForeignKey(StatusPedido, on_delete=models.SET_NULL, null=True, blank=True, default="")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default="")


class ItensPedido(models.Model):
    numero_pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True, default="", related_name='itens')
    item = models.ForeignKey(ItemCardapio, on_delete=models.SET_NULL, null=True, blank=True, default="")
    observacao = models.CharField(max_length=100, null=True, blank=True)

    quantidade = models.IntegerField(null=False, blank=False, default=0)
    valor_unitario = models.FloatField(null=False)
    valor_total_item = models.FloatField(null=False)
