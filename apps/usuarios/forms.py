from django import forms

class LoginForm(forms.Form):
    nome_usuario = forms.CharField(
        label='Usuário',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    senha_usuario = forms.CharField(
        label='Senha',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )