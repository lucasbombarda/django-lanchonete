from django import forms
from .models import ItemCardapio

class ItemCardapioForm(forms.ModelForm):
    class Meta:
        model = ItemCardapio
        exclude = [
            'criado_em',
        ]