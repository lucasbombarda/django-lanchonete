from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.forms import inlineformset_factory

from datetime import datetime

from .forms import CabecalhoPedidoForm, ItemPedidoFormSet, ItemPedidoForm, EditarStatusPedidoForm, FecharPedidoForm

from apps.cardapio.models import ItemCardapio

from .models import Pedido, ItensPedido, StatusPedido


@login_required(login_url='usuarios:login', redirect_field_name='next')
def home_pedidos(request):
    pedidos = Pedido.objects.filter(status=1).order_by("criado_em")
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

    if not item_formset.is_valid() or all([not form.cleaned_data for form in item_formset.forms]):
        messages.error(request, "Erro, favor preencher pelo menos um item.")
        return redirect('pedido:novo_pedido')

    # TODO: FIX THIS!
    if cabecalho_form.is_valid() and item_formset.is_valid():
        # Salva o objeto CabecalhoPedido
        cabecalho = cabecalho_form.save(commit=False)

        status = StatusPedido.objects.get(pk=1)
        status_pedido = cabecalho_form.cleaned_data['status'] = status
        cabecalho.status = status_pedido

        atendente = cabecalho_form.cleaned_data['usuario'] = request.user
        cabecalho.usuario = atendente

        valor_total_pedido = 0  # Inicializa a variável com zero

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

            valor_total_pedido += valor_total_item


        cabecalho.valor_total = valor_total_pedido
        cabecalho.save()

        for item_form in item_formset:
            item = item_form.save(commit=False)
            item.numero_pedido = cabecalho  # Atualiza o campo para referenciar o cabeçalho salvo
            item.save()

        messages.success(request, "Pedido adicionado com sucesso!")

    else:
        messages.error(request, "Erro, favor corrigir.")
        return redirect('pedido:novo_pedido')

    return redirect('pedido:home')

@login_required(login_url='usuarios:login', redirect_field_name='next')
@permission_required('pedido.fechar_pedido', raise_exception=True)
def imprimir_pedido(request, id):
    pedido = Pedido.objects.filter(pk=id).first()
    itens = ItensPedido.objects.filter(numero_pedido=id)

    context = {'pedido': pedido, 'itens': itens}
    return render(request, 'pedido/pages/impressao.html', context=context)

@login_required(login_url='usuarios:login', redirect_field_name='next')
@permission_required('pedido.fechar_pedido', raise_exception=True)
def imprimir_cozinha(request, id):
    pedido = Pedido.objects.filter(pk=id).first()
    itens = ItensPedido.objects.filter(numero_pedido=id)

    context = {'pedido': pedido, 'itens': itens}
    return render(request, 'pedido/pages/impressao_cozinha.html', context=context)

@login_required(login_url='usuarios:login', redirect_field_name='next')
def editar_pedido(request, id):
    pedido = Pedido.objects.filter(pk=id).first()

    item_pedido_formset = inlineformset_factory(Pedido, ItensPedido, form=ItemPedidoForm, extra=0, can_delete=True)
    cabecalho_form = CabecalhoPedidoForm(data=request.POST or None, instance=pedido)
    itens_formset = item_pedido_formset(data=request.POST or None, instance=pedido, prefix='itens_pedido')
    if request.method == "POST":

        if cabecalho_form.is_valid() and itens_formset.is_valid():
            cabecalho = cabecalho_form.save(commit=False)

            valor_total_pedido = 0  # Inicializa a variável com zero

            # Itera pelos objetos ItemPedido e atualiza o campo numero_pedido
            for item_form in itens_formset:
                item = item_form.save(commit=False)
                item.numero_pedido = cabecalho
                id_item = item_form.cleaned_data['item'].id
                valor_unitario = ItemCardapio.objects.get(pk=id_item).preco_unitario
                quantidade = item_form.cleaned_data['quantidade']
                valor_total_item = round(valor_unitario * quantidade, 2)
                item.valor_unitario = valor_unitario
                item.valor_total_item = valor_total_item

                valor_total_pedido += valor_total_item

            cabecalho.valor_total = valor_total_pedido
            cabecalho.save()

            for item_form in itens_formset:
                item = item_form.save(commit=False)
                item.numero_pedido = cabecalho  # Atualiza o campo para referenciar o cabeçalho salvo
                item.save()

            messages.success(request, f"Pedido {pedido.pk} atualizado com sucesso!")
            
            return redirect('pedido:home')
        else:
            messages.error(request, "Erro, favor corrigir.")

    context = {'cabecalho_form': cabecalho_form, 'itens_formset': itens_formset}
    return render(request, 'pedido/pages/editar_pedido.html', context=context)

@login_required(login_url='usuarios:login', redirect_field_name='next')
@permission_required('pedido.fechar_pedido', raise_exception=True)
def editar_status(request, id):
    pedido = Pedido.objects.filter(pk=id).first()
    status_pedido_form = EditarStatusPedidoForm(data=request.POST or None, instance=pedido)

    if request.method == "POST":
        if status_pedido_form.is_valid():
            status_pedido_form.save()
            messages.success(request, "Status atualizado com sucesso!")
            return redirect('pedido:home')
        else:
            messages.error(request, "Erro, favor ajustar.")

    context = {"form": status_pedido_form}

    return render(request, 'pedido/pages/editar_status.html', context=context)

@login_required(login_url='usuarios:login', redirect_field_name='next')
@permission_required('pedido.fechar_pedido', raise_exception=True)
def fechar_pedido(request, id):
    pedido = Pedido.objects.filter(pk=id).first()
    itens = ItensPedido.objects.filter(numero_pedido=id)

    form_fechar_pedido = FecharPedidoForm(request.POST or None, instance=pedido)
    
    if request.method == "POST":
        if form_fechar_pedido.is_valid():
            pedido.fechado_por = request.user

            status = StatusPedido.objects.get(pk=2)
            pedido.status = status

            agora = datetime.now()
            pedido.fechado_em = agora

            form_fechar_pedido.save()
            pedido.save()

            messages.success(request, "Pedido fechado com sucesso!")
            return redirect('pedido:home')
        else:
            messages.error(request, "ERRO!")
    else:
        form_fechar_pedido = FecharPedidoForm(instance=pedido)

    context = {'pedido': pedido, 'itens': itens, 'form_fechar_pedido': form_fechar_pedido}
    return render(request, 'pedido/pages/fechar_pedido.html', context=context)

@login_required(login_url='usuarios:login', redirect_field_name='next')
@permission_required('pedido.fechar_pedido', raise_exception=True)
def listar_pedidos(request):

    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    
    if not data_inicio and not data_fim:
        data_inicio = str(datetime.today().date()) + " 00:00"
        data_fim = str(datetime.today().date()) + " 23:59"


    pedidos = Pedido.objects.filter(criado_em__range=[data_inicio, data_fim])
    itens = ItensPedido.objects.filter(numero_pedido__criado_em__range=[data_inicio, data_fim])

    context = {"pedidos": pedidos, "itens": itens}
    return render(request, 'pedido/pages/filtro_pedido.html', context=context)