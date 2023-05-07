from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CabecalhoPedidoForm, ItemPedidoFormSet

from apps.cardapio.models import ItemCardapio

from .models import Pedido


@login_required(login_url='usuarios:login', redirect_field_name='next')
def home_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedido/pages/pedidos.html', context={"pedidos": pedidos})

@login_required(login_url='usuarios:login', redirect_field_name='next')
def novo_pedido(request):
    form = CabecalhoPedidoForm(prefix='cabecalho_pedido')
    formset = ItemPedidoFormSet(prefix='itens_pedido')
    return render(request, 'pedido/pages/novo_pedido.html', context={"form": form, "formset": formset})

@login_required(login_url='usuarios:login', redirect_field_name='next')
def confirmar_pedido(request):
    cabecalho_form = CabecalhoPedidoForm(request.POST, prefix='cabecalho_pedido')
    item_formset = ItemPedidoFormSet(request.POST, prefix='itens_pedido')


    # TODO: FIX THIS!
    if cabecalho_form.is_valid() and item_formset.is_valid():
        # Salva o objeto CabecalhoPedido
        cabecalho = cabecalho_form.save()

        # Itera pelos objetos ItemPedido e atualiza o campo numero_pedido
        for item_form in item_formset:
            item = item_form.save(commit=False)
            item.numero_pedido = cabecalho
            id_item = item_form.cleaned_data['item'].id
            valor_unitario = ItemCardapio.objects.get(pk=id_item).preco_unitario
            quantidade = item_form.cleaned_data['quantidade']
            valor_total_item = round(valor_unitario * quantidade, 2)
            item.valor_unitario = valor_unitario
            item.valor_total_item = valor_total_item
            item.save()

        messages.success(request, "Pedido adicionado com sucesso!")

    return redirect('pedido:home')