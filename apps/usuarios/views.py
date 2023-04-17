from django.shortcuts import render, redirect

from .forms import LoginForm
from django.contrib import auth
from django.contrib import messages

# Create your views here.
def login(request):
    form = LoginForm()
    request.session["autenticado"] = False
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            nome = form["nome_usuario"].value()
            senha = form["senha_usuario"].value()

            usuario = auth.authenticate(request, username=nome, password=senha)

            if usuario:
                auth.login(request, usuario)
                messages.success(request, "Autenticado!")
                request.session["autenticado"] = True
                return redirect('cardapio:home')
            else:
                messages.error(request, "Usuário e/ou senha incorretos!")
                request.session["autenticado"] = False
                return redirect('usuarios:login')

    return render(request, 'usuarios/pages/login.html', context={"form": form, "message":messages, "is_authenticated": request.user.is_authenticated})

def logout(request):
    auth.logout(request)
    messages.info(request, "Deslogado!")
    request.session["autenticado"] = False
    
    return render(request, 'usuarios/pages/logout.html', context={"message":messages})