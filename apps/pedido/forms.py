from django import forms
from .models import Pedido, ItensPedido
from django.forms import inlineformset_factory


class CabecalhoPedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido

        fields = ["numero_mesa", "observacao"]

        labels = {
            'numero_mesa': 'Número da mesa',
            'observacao': 'Observação',
        }

        widgets = {
            'numero_mesa': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }),

            'observacao': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }),
        }

class ItemPedidoForm(forms.ModelForm):

    class Meta:
        model = ItensPedido

        fields = ["item", "quantidade"]


ItemPedidoFormSet = inlineformset_factory(Pedido, ItensPedido, form=ItemPedidoForm, extra=1, can_delete=True)