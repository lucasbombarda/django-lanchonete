from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages

from .models import ItemCardapio
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
    form = ItemCardapioForm(POST)

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

def listar_todos_itens_cardapio_para_editar(request):
    itenscardapio = ItemCardapio.objects.all().order_by('id')
    return render(request, 'cardapio/pages/editar_item_cardapio.html', context={"itenscardapio": itenscardapio})

def editar_item_cardapio(request, id):
    item = ItemCardapio.objects.filter(id=id)
    return render(request, 'cardapio/pages/form_editar_item_cardapio.html', context={'item': item})