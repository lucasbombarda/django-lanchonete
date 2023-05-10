from django import forms
from .models import Pedido, ItensPedido
from django.forms import inlineformset_factory


class CabecalhoPedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido

        fields = ["numero_mesa",]

        labels = {
            'numero_mesa': 'Número da mesa',
        }

        widgets = {
            'numero_mesa': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }),
        }

class ItemPedidoForm(forms.ModelForm):

    class Meta:
        model = ItensPedido

        fields = ["item", "quantidade", "observacao"]
        
        labels = {
            "item": "Item",
            "quantidade": "Quantidade",
            "observacao": "Observação",
        }

        widgets = {
            'item': forms.Select(
                attrs={
                    'class': 'form-control',
                }),
            'quantidade': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }),
            'observacao': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
        }


ItemPedidoFormSet = inlineformset_factory(Pedido, ItensPedido, form=ItemPedidoForm, extra=1, can_delete=True)