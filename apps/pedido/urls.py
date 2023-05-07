from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('', views.home_pedidos, name="home"),
    path('novo', views.novo_pedido, name="novo_pedido"),
    path('novo/confirmar', views.confirmar_pedido, name="confirmar_pedido"),
]
