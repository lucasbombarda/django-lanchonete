from django.shortcuts import render

def home(request):
    return render(request, 'cardapio/pages/index.html')