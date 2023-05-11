from django.db import models
from django.contrib.auth.models import User
from apps.cardapio.models import ItemCardapio

# Create your models here.
class FormaPagamento(models.Model):
    situacao = models.BooleanField(default=True)
    descricao = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.descricao

class StatusPedido(models.Model):
    situacao = models.BooleanField(default=True)
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
    fechado_em = models.DateTimeField(null=True, blank=True)

    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.SET_NULL, null=True, blank=True, default="")
    status = models.ForeignKey(StatusPedido, on_delete=models.PROTECT, null=False, blank=False)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default="")
    fechado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default="", related_name='fechado_por')

    class Meta:
        permissions = [
            ("fechar_pedido", "Pode fechar pedidos"),
        ]

class ItensPedido(models.Model):
    numero_pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, null=False, blank=False, related_name='itens')
    item = models.ForeignKey(ItemCardapio, on_delete=models.PROTECT, null=False, blank=False)
    observacao = models.CharField(max_length=100, null=True, blank=True)

    quantidade = models.IntegerField(null=False, blank=False, default=0)
    valor_unitario = models.FloatField(null=False)
    valor_total_item = models.FloatField(null=False)
