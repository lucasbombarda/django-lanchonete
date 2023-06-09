from django.urls import path
from django.shortcuts import redirect
from . import views
from django.conf.urls import handler403

app_name = 'cardapio'

urlpatterns = [
    path("", views.home, name="home"),
    path("cardapio/", lambda redir: redirect('cardapio:home'), name="cardapio"),

    # item
    path("cardapio/cadastro", views.cadastro_cardapio, name="cardapio_cadastro"),
    path("cardapio/cadastro/criar", views.criar_item_cardapio, name="cardapio_criar"),
    path("cardapio/cadastro/editar", views.listar_todos_itens_cardapio_para_editar, name='selecionar_item_edicao'),
    path("cardapio/cadastro/<int:id>/editar", views.editar_item_cardapio, name='editar_item'),

    # tipo
    path("cardapio/cadastro/tipo", views.cadastro_tipo, name='cardapio_cadastro_tipo'),
    path("cardapio/cadastro/tipo/criar", views.criar_tipo_item, name='cardapio_tipo_criar'),
    path("cardapio/cadastro/tipo/editar", views.listar_todos_tipos_itens_para_editar, name='selecionar_tipo_item_edicao'),
    path("cardapio/cadastro/tipo/<int:id>/editar", views.editar_tipo_item_cardapio, name='editar_tipo_item'),
]

handler403 = 'apps.cardapio.views.custom_403'
