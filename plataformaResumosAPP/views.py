from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm 

def register(request):
    if request.method == 'GET':
        ...

def login_view(request):
    if request.method == 'GET':
        ...
'''
def login_view(request):
    if request.user.is_authenticated:
        # Se o usuário já estiver logado, redireciona para a home ou dashboard
        return redirect('dashboard') # Crie uma URL chamada 'dashboard'
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # 1. Autentica o usuário com base nas credenciais
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # 2. Se a autenticação for bem-sucedida, inicia a sessão
                login(request, user)
                
                # 3. Redirecionamento baseado no tipo de usuário
                if user.user_type == 'ADMIN':
                    return redirect('admin_dashboard')
                elif user.user_type == 'REVISOR':
                    return redirect('revisor_dashboard')
                else:
                    return redirect('autor_dashboard') 
            else:
                # Se as credenciais estiverem incorretas
                return render(request, 'login.html', {'form': form, 'error_message': 'Credenciais inválidas.'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
    '''