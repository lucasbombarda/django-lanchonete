from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib import auth

# Create your views here.
def login(request):
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            nome = form["nome_usuario"].value()
            senha = form["senha_usuario"].value()

            usuario = auth.authenticate(request, username=nome, password=senha)

            if usuario:
                auth.login(request, usuario)
                return redirect('cardapio:home')
            else:
                return redirect('usuarios:login')

    return render(request, 'usuarios/pages/login.html', context={"form": form})

