from django import forms
from django.contrib.auth.forms import UserCreationForm 
from .models import CustomUser 


class LoginForm(forms.Form):

    username = forms.CharField(
        label='Usuário (ou E-mail)',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu usuário ou e-mail'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Sua senha'})
    )


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        # Campos que o usuário deve preencher.
        # O AbstractUser já inclui username e password.
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type')
        
    # Remove o campo user_type ou o torna um campo oculto com valor padrão
    # para que o usuário se cadastre sempre como 'AUTOR'.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Define o user_type como 'AUTOR' e o esconde do usuário
        self.initial['user_type'] = 'AUTOR'
        self.fields['user_type'].widget = forms.HiddenInput()
        
        # Configura as classes de estilo para os campos visíveis (opcional)
        for field_name in ['username', 'email', 'nome_completo']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})