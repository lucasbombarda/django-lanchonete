from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import CabecalhoPedidoForm, ItemPedidoFormSet


@login_required(login_url='usuarios:login', redirect_field_name='next')
def home_pedidos(request):
    return render(request, 'pedido/pages/pedidos.html')


def novo_pedido(request):
    form = CabecalhoPedidoForm()
    formset = ItemPedidoFormSet
    return render(request, 'pedido/pages/novo_pedido.html', context={"form": form, "formset": formset})