from django.shortcuts import render

from .models import ItemCardapio

def home(request):
    itenscardapio = ItemCardapio.objects.filter(ativo=True).order_by('id')
    return render(request, 'cardapio/pages/index.html', context={'itenscardapio':itenscardapio})