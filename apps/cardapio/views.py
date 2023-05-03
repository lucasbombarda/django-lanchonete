from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages

from .models import ItemCardapio, TipoItem
from .forms import ItemCardapioForm, TipoItemForm

def home(request):
    itenscardapio = ItemCardapio.objects.filter(ativo=True).order_by('id')
    return render(request, 'cardapio/pages/index.html', context={'itenscardapio':itenscardapio})

@login_required(login_url='usuarios:login')
def cadastro_cardapio(request):
    item_cardapio = request.session.get('formulario_cadastro_item_cardapio', None)
    form = ItemCardapioForm(item_cardapio)
    
    return render(request, 'cardapio/pages/cadastro_cardapio.html', context={'form': form})


@login_required(login_url='usuarios:login')
def criar_item_cardapio(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST

    request.session['formulario_cadastro_item_cardapio'] = POST
    form = ItemCardapioForm(POST, files=request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, 'Item adicionado com sucesso!')
        del(request.session['formulario_cadastro_item_cardapio'])
        
    return redirect('cardapio:cardapio_cadastro')

@login_required(login_url='usuarios:login')
def cadastro_tipo(request):
    form = TipoItemForm()
    return render(request, 'cardapio/pages/cadastro_tipo_item.html', context={'form': form})

@login_required(login_url='usuarios:login')
def criar_tipo_item(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST

    request.session['formulario_cadastro_tipo_item'] = POST
    form = TipoItemForm(POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'Tipo adicionado com sucesso!')
        del(request.session['formulario_cadastro_tipo_item'])

    return redirect('cardapio:cardapio_cadastro_tipo')

@login_required(login_url='usuarios:login')
def listar_todos_itens_cardapio_para_editar(request):
    itenscardapio = ItemCardapio.objects.all().order_by('id')
    return render(request, 'cardapio/pages/editar_item_cardapio.html', context={"itenscardapio": itenscardapio})

@login_required(login_url='usuarios:login')
def editar_item_cardapio(request, id):
    item = ItemCardapio.objects.filter(pk=id).first()
    form = ItemCardapioForm(
        data=request.POST or None, 
        files=request.FILES or None,
        instance=item)

    if form.is_valid():
        item = form.save()
        messages.success(request, "Item editado com sucesso!")

    return render(request, 'cardapio/pages/form_editar_item_cardapio.html', context={'form': form})

@login_required(login_url='usuarios:login')
def listar_todos_tipos_itens_para_editar(request):
    situacoes = TipoItem.objects.all().order_by('id')
    return render(request, 'cardapio/pages/editar_tipo_item.html', context={"situacoes": situacoes})


@login_required(login_url='usuarios:login')
def editar_tipo_item_cardapio(request, id):
    tipo = TipoItem.objects.filter(pk=id).first()
    form = TipoItemForm(
        data=request.POST or None, 
        instance=tipo)

    if form.is_valid():
        tipo = form.save()
        messages.success(request, "Tipo editado com sucesso!")

    return render(request, 'cardapio/pages/form_editar_tipo_item.html', context={'form': form})
