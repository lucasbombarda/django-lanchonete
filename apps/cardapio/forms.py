from django import forms
from .models import ItemCardapio, TipoItem

class ItemCardapioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tipos_ativos = TipoItem.objects.filter(ativo=True)
        self.fields['tipo'].queryset = tipos_ativos

    class Meta:
        model = ItemCardapio

        fields = [
            'ativo',
            'tipo',
            'numero',
            'nome',
            'descricao',
            'preco_unitario',
            'imagem'
        ]

        labels = {
            'ativo': 'Situação',
            'numero': 'Número no cardápio',
            'nome': 'Nome',
            'descricao': 'Descrição',
            'preco_unitario': 'Preço',
        }

        error_messages = {
            'numero': {
                'unique': 'O número informado já existe no cardápio.'
            },
        }

        widgets = {
            'ativo': forms.CheckboxInput(),
            'numero': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }),
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }),
            'descricao': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }),
            'preco_unitario': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }),
            'tipo': forms.Select(
                attrs={
                    'class': 'form-control',
                }),
            'imagem': forms.FileInput(attrs={
                    'class': 'form-control',
                }),
        }

class TipoItemForm(forms.ModelForm):
    class Meta:
        model = TipoItem
        fields = '__all__'
        labels = {
            'ativo': 'Situação',
            'nome': 'Nome',
        }

        widgets = {
            'ativo': forms.CheckboxInput(),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }