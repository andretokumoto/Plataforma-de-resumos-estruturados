import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UsuarioCreationForm, CriacaoTurma, InscricaoEmTurma, ProjetoForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Turma, Semestre, Inscricao, Projeto, Programa, ODS
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
    
    lista_inscricoes = Inscricao.objects.filter(aluno=request.user)
    return render(request, 'aluno/dashboard_aluno.html', {'lista_inscricoes': lista_inscricoes})

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
            try:
                turma_requerida = Turma.objects.get(codigo_acesso=codigo_acesso)
                
                
                if Inscricao.objects.filter(aluno=request.user, turma=turma_requerida).exists():
                    return render(request, "aluno/ja_incrito.html", {
                        "mensagem": "Você já está matriculado nesta turma."
                    })

                
                Inscricao.objects.create(aluno=request.user, turma=turma_requerida)
                return redirect('dashboard_aluno')

            except Turma.DoesNotExist:
                messages.error(request, "Código de turma inválido.")
    else:
        form = InscricaoEmTurma()
    return render(request, "aluno/inscricao_turma.html", {"form": form})


@login_required
def relatorio_view(request, inscricao_id):

    inscricao = get_object_or_404(Inscricao, id=inscricao_id, aluno=request.user)

    prog1, _ = Programa.objects.get_or_create(nome="Educação e Sustentabilidade")
    prog2, _ = Programa.objects.get_or_create(nome="Tecnologia e Inovação para o Desenvolvimento Social")
    
    for i in range(1, 18):
        ODS.objects.get_or_create(numero=i, defaults={'nome': f'Objetivo de Desenvolvimento Sustentável {i}'})

    projeto, criado = Projeto.objects.get_or_create(
        aluno=request.user,
        turma=inscricao.turma,
        defaults={
            'titulo_projeto': f"Projeto - {inscricao.turma.nome_turma}",
            'nome_autores': request.user.get_full_name() or request.user.username,
        }
    )

    if criado:
        projeto.programa.add(prog1)

    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados do relatório salvos com sucesso!")
            return redirect('relatorio_projeto', inscricao_id=inscricao.id)
        else:
            messages.error(request, "Erro ao salvar. Verifique os campos (ODS: mínimo 1, máximo 3).")
    else:
 
        form = ProjetoForm(instance=projeto)

    return render(request, "aluno/relatorio.html", {
        "projeto": projeto,
        "form": form
    })