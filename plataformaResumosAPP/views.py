import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UsuarioCreationForm, CriacaoTurma, InscricaoEmTurma, ProjetoForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Turma, Semestre, Inscricao, Projeto, Programa, ODS, Submissao
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
                form.add_error(None, "Usuário ou senha incorretos.")

    return render(request, 'login.html', {'form': form})


def cadastro_view(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça o login.")
            return redirect('login')
    else:
        form = UsuarioCreationForm()
    return render(request, 'cadastro.html', {'form': form})


@login_required
def dashboard_aluno(request):
    if request.user.tipo_usuario != 1:
        return HttpResponseForbidden()
    
   
    lista_inscricoes = Inscricao.objects.filter(aluno=request.user)
    

    for inscricao in lista_inscricoes:
        inscricao.projeto_vinculado = Projeto.objects.filter(aluno=request.user, turma=inscricao.turma).first()
    
    return render(request, 'aluno/dashboard_aluno.html', {
        'lista_inscricoes': lista_inscricoes
    })


@login_required
def dashboard_professor(request):
    if request.user.tipo_usuario != 2:
        return HttpResponseForbidden()
    
    lista_turmas = Turma.objects.filter(responsavel=request.user)

 
    return render(request, 'professor/dashboard_professor.html', {'lista_turmas':lista_turmas} )


@login_required
def dashboard_coordenador(request):
    if request.user.tipo_usuario != 3:
        return HttpResponseForbidden()
    return render(request, 'coordenador/dashboard_coordenador.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def criar_turma_view(request):
    if request.user.tipo_usuario != 2:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CriacaoTurma(request.POST)
        if form.is_valid():
            turma = form.save(commit=False)
            turma.professor = request.user
            
            # Gerador de codigo de acesso aleatorio com 6 digitos
            while True:
                codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                if not Turma.objects.filter(codigo_acesso=codigo).exists():
                    break
            
            turma.codigo_acesso = codigo
            turma.save()
            messages.success(request, f"Turma criada com sucesso! Código de acesso: {codigo}")
            return redirect('dashboard_professor')
    else:
        form = CriacaoTurma()

    return render(request, 'professor/criar_turma.html', {'form': form})


@login_required
def inscrever_em_turma_view(request):
    if request.user.tipo_usuario != 1:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = InscricaoEmTurma(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo_acesso']
            try:
                turma = Turma.objects.get(codigo_acesso=codigo)
                
                # Cria a inscricao vinculando o aluno e a turma encontrada pelo codigo
                Inscricao.objects.create(aluno=request.user, turma=turma)
                messages.success(request, f"Inscrição realizada com sucesso na turma: {turma.nome_turma}")
                return redirect('dashboard_aluno')
                
            except Turma.DoesNotExist:
                messages.error(request, "Código de acesso inválido.")
            except IntegrityError:
                messages.error(request, "Você já está inscrito nesta turma.")
    else:
        form = InscricaoEmTurma()

    return render(request, 'aluno/inscricao_turma.html', {'form': form})


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
            'nome_autores': request.user.get_full_name(),
        }
    )

    if criado:
        projeto.programa.add(prog1)

    if request.method == 'POST':
  
        if projeto.status_projeto not in [0, 3]:
            messages.error(request, "Este relatório não pode ser editado pois já foi submetido.")
            return redirect('relatorio_projeto', inscricao_id=inscricao.id)

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


@login_required
def submissao_view(request, projeto_id):
    if request.user.tipo_usuario != 1:
        return HttpResponseForbidden()
    
    projeto = get_object_or_404(Projeto, id=projeto_id, aluno=request.user)
    
   
    if projeto.status_projeto in [0, 3]:
        projeto.status_projeto = 1  # Define como "Em análise"
        projeto.save()
        
        Submissao.objects.create(
            projeto=projeto,
            resultado_submissao=0
        )
        messages.success(request, "Projeto submetido com sucesso!")
    else:
        messages.error(request, "Este projeto não pode ser submetido no momento.")
        
    return redirect('dashboard_aluno')

@login_required
def painel_turma_view(request, turma_id):
    if request.user.tipo_usuario != 2:
        return HttpResponseForbidden()

    #busca tirmas dos professores
    turma = get_object_or_404(
        Turma,
        id=turma_id,
        responsavel=request.user
    )

    # Busca projetos da turma
    projetos = Projeto.objects.filter(
        turma=turma,
        submissoes__isnull=False
    ).select_related(
        'aluno'
    ).distinct().order_by(
        'aluno__first_name',
        'aluno__username'
)

    return render(request, 'professor/painel_turma.html', {
        'turma': turma,
        'projetos': projetos
    })

@login_required
def projeto_analise_view(request):
    return render(request, "professor/projeto_aluno.html")