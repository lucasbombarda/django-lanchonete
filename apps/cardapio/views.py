from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import ItemCardapio
from .forms import ItemCardapioForm

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
        
    return redirect('cardapio:cardapio_cadastro')