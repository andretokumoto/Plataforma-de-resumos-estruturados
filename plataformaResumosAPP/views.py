from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UsuarioCreationForm
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username_input = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # se login com email:
            # procura usuario pelo email no banco de dados para fazer a autenticação
            if '@' in username_input:
                try:
                    user_obj = User.objects.get(email=username_input)
                    username = user_obj.username
                except User.DoesNotExist:
                    username = username_input
            else:
                username = username_input

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('home') 

            else:
                form.add_error(None, 'Usuário ou senha inválidos')

    return render(request, 'login.html', {'form': form})

def cadastro_view(request):
    form = UsuarioCreationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            messages.success(request, 'Cadastro realizado com sucesso! ')
            return redirect('login')

    if not form.is_valid():
        print(form.errors)

    return render(request, 'cadastro.html', {'form': form})