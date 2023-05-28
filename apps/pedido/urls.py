from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('', views.home_pedidos, name="home"),
    path('novo', views.novo_pedido, name="novo_pedido"),
    path('novo/confirmar', views.confirmar_pedido, name="confirmar_pedido"),
    path('imprimir/<int:id>', views.imprimir_pedido, name="imprimir"),
<<<<<<< HEAD
    path('imprimir/cozinha/<int:id>', views.imprimir_cozinha, name="imprimir_cozinha"),
    path('editar/<int:id>', views.editar_pedido, name="editar_pedido"),
    path('editar/status/<int:id>', views.editar_status, name="editar_status"),
    path('fechar/<int:id>', views.fechar_pedido, name="fechar_pedido"),
    
    path('listar', views.listar_pedidos, name="listar_pedido"),
=======
    path('imprimir/cozinha/<int:id>',
         views.imprimir_cozinha, name="imprimir_cozinha"),
    path('editar/<int:id>', views.editar_pedido, name="editar_pedido"),
    path('editar/status/<int:id>', views.editar_status, name="editar_status"),
    path('fechar/<int:id>', views.fechar_pedido, name="fechar_pedido"),

    path('listar', views.listar_pedidos, name="listar_pedido"),
    path('buscar', views.buscar_pedidos, name="buscar_pedido"),
>>>>>>> servidor/master
]
