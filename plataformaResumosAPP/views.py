import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UsuarioCreationForm, CriacaoTurma, InscricaoEmTurma
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Turma, Semestre, Inscricao
from django.db import IntegrityError

User = get_user_model()


def login_view(request):

    form = LoginForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():

            username_input = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Login usando email
            if '@' in username_input:
                try:
                    user_obj = User.objects.get(
                        email=username_input
                    )
                    username = user_obj.username

                except User.DoesNotExist:
                    username = username_input

            else:
                username = username_input

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:

                login(request, user)

                #Redirecionamento para dashboard por tipo de usuario
                if user.tipo_usuario == 1:
                    return redirect('dashboard_aluno')

                elif user.tipo_usuario == 2:
                    return redirect('dashboard_professor')

                elif user.tipo_usuario == 3:
                    return redirect('dashboard_coordenador')

                else:
                    return redirect('login')

            else:
                form.add_error(
                    None,
                    'Usuário ou senha inválidos'
                )

    return render(
        request,
        'login.html',
        {'form': form}
    )

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



@login_required
def dashboard_aluno(request):

    if request.user.tipo_usuario != 1:
        return HttpResponseForbidden()

    return render(request, 'aluno/dashboard_aluno.html')


@login_required
def dashboard_professor(request):

    if request.user.tipo_usuario != 2:
        return HttpResponseForbidden()

    return render(request, 'professor/dashboard_professor.html')


@login_required
def dashboard_coordenador(request):

    if request.user.tipo_usuario != 3:
        return HttpResponseForbidden()

    return render(request, 'coordenador/dashboard_coordenador.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def gerar_codigo_unico():

    while True:

        codigo = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=6
            )
        )

        if not Turma.objects.filter(
            codigo_acesso=codigo
        ).exists():

            return codigo
        

@login_required
def dashboard_professor(request):

    if request.user.tipo_usuario != 2:
        return HttpResponseForbidden()

    return render(request, 'professor/dashboard_professor.html')

@login_required
def criar_turma_view(request):


    if request.user.tipo_usuario != 2:
        return HttpResponseForbidden()

    try:
        semestre_ativo = Semestre.objects.latest('id')

    except Semestre.DoesNotExist:
        return HttpResponseForbidden(
            "Nenhum semestre cadastrado."
        )

    if request.method == 'POST':

        form = CriacaoTurma(request.POST)

        if form.is_valid():

            turma = form.save(commit=False)

            turma.responsavel = request.user

            turma.semestre = semestre_ativo

            turma.codigo_acesso = gerar_codigo_unico()

            turma.save()

            return redirect('dashboard_professor')

    else:

        form = CriacaoTurma()

    return render(
        request,
        'professor/criar_turma.html',
        {'form': form}
    )

@login_required
def inscrever_em_turma_view(request):
    

    if request.method == 'POST':

        form = InscricaoEmTurma(request.POST)

        if form.is_valid():

            codigo_acesso = form.cleaned_data['codigo_acesso']
            aluno = request.user

            try:

                turma_requerida = Turma.objects.get(codigo_acesso = codigo_acesso)

                matricula = Inscricao.objects.create(
                    aluno = aluno,
                    turma = turma_requerida
                )

                return render(request, "aluno/relatorio.html", {
                    "mensagem": "Inscrição realizada com sucesso!"
                })
            


            except Inscricao.DoesNotExist:
                return HttpResponseForbidden(
                    "Nenhum semestre cadastrado."
                )
            
            except IntegrityError:
                return render(request, "aluno/ja_incrito.html", {
                    "mensagem": "Você já está inscrito nessa turma"
                })
    else:
        form = InscricaoEmTurma()

    return render(request, "aluno/inscricao_turma.html", {"form": form})
