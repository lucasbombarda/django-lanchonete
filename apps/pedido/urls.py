from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('', views.home_pedidos, name="home"),
]
