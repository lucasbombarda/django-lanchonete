from django import forms
from django.core.exceptions import PermissionDenied
from .models import Pedido, ItensPedido, FormaPagamento, StatusPedido
from django.forms import inlineformset_factory

from apps.cardapio.models import ItemCardapio


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
    def clean_numero_mesa(self):
        numero_mesa = self.cleaned_data['numero_mesa']
        if numero_mesa < 0:
            raise forms.ValidationError('O número da mesa deve ser maior ou igual a zero.')
        return numero_mesa

class ItemPedidoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        itens_ativos = ItemCardapio.objects.filter(ativo=True)
        self.fields['item'].queryset = itens_ativos
    
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
                    'required': 'required',
                },
                ),
            'quantidade': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }),
            'observacao': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
        }
    
    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        if quantidade <= 0:
            raise forms.ValidationError('A quantidade deve ser maior do que zero.')
        return quantidade

class EditarStatusPedidoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        status = StatusPedido.objects.filter(situacao=True)
        self.fields['status'].queryset = status

    class Meta:
        model = Pedido

        fields = ['status',]

        widgets = {
            'status': forms.Select(
            attrs={
                'class': 'form-control'
            }),
        }


class FecharPedidoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        forma_pagamento = FormaPagamento.objects.filter(situacao=True)
        self.fields['forma_pagamento'].queryset = forma_pagamento

    class Meta:
        model = Pedido

        fields = ['forma_pagamento',]

        labels = {
            "forma_pagamento": "Forma de pagamento",
        }

        widgets = {
            'forma_pagamento': forms.Select(
            attrs={
                'class': 'form-control',
                'required': 'required',
            }),
        }

        def clean(self):
            cleaned_data = super().clean()
            user = self.request.user
            if not user.has_perm("pedido.fechar_pedido"):
                raise PermissionDenied("Você não tem permissão para fechar pedidos.")
            return cleaned_data

ItemPedidoFormSet = inlineformset_factory(Pedido, ItensPedido, form=ItemPedidoForm, extra=1, can_delete=True)