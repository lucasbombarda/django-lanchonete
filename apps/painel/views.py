from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='usuarios:login', redirect_field_name='next')
def home_painel(request):
    return render(request, 'painel/pages/index.html')