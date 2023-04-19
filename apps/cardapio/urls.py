from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'cardapio'

urlpatterns = [
    path("", views.home, name="home"),
    path("cardapio/", lambda redir: redirect('cardapio:home'), name="cardapio"),
    path("cardapio/cadastro", views.cadastro_cardapio, name="cardapio_cadastro"),
    path("cardapio/cadastro/criar", views.criar_item_cardapio, name="cardapio_criar"),
]
