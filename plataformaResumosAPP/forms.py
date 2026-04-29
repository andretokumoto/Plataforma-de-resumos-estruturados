from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Turma

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
        fields = ('username', 'email', 'first_name', 'last_name', 'ra')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in ['username', 'email', 'first_name', 'last_name', 'ra']:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

    def save(self, commit=True):
        user = super().save(commit=False)

        user.tipo_usuario = 1

        if commit:
            user.save()

        return user
    

    
class CriacaoTurma(forms.ModelForm):

    class Meta:

        model = Turma

        fields = (
            'nome_turma',
            'disciplina',
            'curso',
        )

        labels = {
            'nome_turma': 'Nome da Turma',
            'disciplina': 'Unidade Curricular',
            'curso': 'Curso Graduação',
        }

        widgets = {

            'nome_turma': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'disciplina': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'curso': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

        }