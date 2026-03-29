from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário (ou E-mail)',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu usuário ou e-mail'
        })
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sua senha'
        })
    )


class UsuarioCreationForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'ra')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # suário se cadastra como ALUNO
        self.initial['tipo_usuario'] = 1
        self.fields['tipo_usuario'].widget = forms.HiddenInput()

       
        for field_name in ['username', 'email', 'first_name', 'last_name', 'ra']:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })