from django.contrib import admin
from .models import (
    Usuario,
    Projeto,
    Submissao,
    Revista,
    Turma,
    Semestre,
    ProjetoPorTurma,
    ProjetosSelecionados
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo_usuario', 'ra')


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo_projeto', 'aluno', 'professor_responsavel', 'status_projeto')


@admin.register(Submissao)
class SubmissaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'projeto', 'resultado_submissao', 'data_submissao')


@admin.register(Revista)
class RevistaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'semestre')


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome_turma', 'responsavel', 'codigo_acesso')


@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ('ano', 'semestre', 'coordenador')


@admin.register(ProjetoPorTurma)
class ProjetoPorTurmaAdmin(admin.ModelAdmin):
    list_display = ('projeto', 'turma', 'aluno')


@admin.register(ProjetosSelecionados)
class ProjetosSelecionadosAdmin(admin.ModelAdmin):
    list_display = ('submissao', 'revista')