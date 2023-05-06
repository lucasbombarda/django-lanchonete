from django.contrib import admin

from .models import Pedido, ItensPedido, FormaPagamento, StatusPedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    ...

@admin.register(ItensPedido)
class ItensPedidoAdmin(admin.ModelAdmin):
    ...

@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    ...

@admin.register(StatusPedido)
class StatusPedidoAdmin(admin.ModelAdmin):
    ...
