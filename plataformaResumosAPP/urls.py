from django.urls import path
from .views import login_view,cadastro_view,dashboard_aluno,dashboard_professor,dashboard_coordenador,logout_view ,criar_turma_view,inscrever_em_turma_view,relatorio_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('cadastro/', cadastro_view, name='cadastro'),
    path('logout/', logout_view, name='logout'),
    path('aluno/', dashboard_aluno, name='dashboard_aluno'),
    path('professor/', dashboard_professor, name='dashboard_professor'),
    path('coordenador/', dashboard_coordenador, name='dashboard_coordenador'),
    path('criarturma/', criar_turma_view, name='criar_turma'),
    path('inscricao/', inscrever_em_turma_view, name='inscrever_em_turma'),
    path('relatorio/<int:inscricao_id>/', relatorio_view, name='relatorio_projeto'),
]