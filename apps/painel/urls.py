from django.urls import path
from . import views

app_name = 'painel'

urlpatterns = [
    path('', views.home_painel, name="home"),
]
