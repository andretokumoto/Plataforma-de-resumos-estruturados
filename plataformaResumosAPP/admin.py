from django.contrib import admin
from .models import (
    Usuario, Semestre, Turma, Projeto,
    Submissao, Revista, ProjetoPorTurma, ProjetosSelecionados
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome_usuario', 'email_usuario', 'tipo_usuario', 'ra')
    list_filter = ('tipo_usuario',)
    search_fields = ('nome_usuario', 'email_usuario', 'ra')


@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ('ano', 'semestre', 'coordenador')
    list_filter = ('ano', 'semestre')
    search_fields = ('ano',)


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome_turma', 'codigo_acesso', 'responsavel')
    search_fields = ('nome_turma', 'codigo_acesso')
    list_filter = ('responsavel',)


class SubmissaoInline(admin.TabularInline):
    model = Submissao
    extra = 0
    readonly_fields = ('data_submissao',)


class ProjetoPorTurmaInline(admin.TabularInline):
    model = ProjetoPorTurma
    extra = 0


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo_projeto', 'usuario', 'status_projeto')
    list_filter = ('status_projeto',)
    search_fields = ('titulo_projeto', 'nome_autores')
    inlines = [SubmissaoInline, ProjetoPorTurmaInline]


@admin.register(Submissao)
class SubmissaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'projeto', 'resultado_submissao', 'data_submissao')
    list_filter = ('resultado_submissao', 'data_submissao')
    search_fields = ('projeto__titulo_projeto',)
    readonly_fields = ('data_submissao',)


@admin.register(Revista)
class RevistaAdmin(admin.ModelAdmin):
    list_display = ('revista_publicada', 'semestre')
    list_filter = ('semestre',)
    search_fields = ('revista_publicada',)


@admin.register(ProjetoPorTurma)
class ProjetoPorTurmaAdmin(admin.ModelAdmin):
    list_display = ('projeto', 'turma', 'aluno')
    list_filter = ('turma',)
    search_fields = ('projeto__titulo_projeto', 'aluno__nome_usuario')


@admin.register(ProjetosSelecionados)
class ProjetosSelecionadosAdmin(admin.ModelAdmin):
    list_display = ('submissao_aceita', 'revista')
    list_filter = ('revista',)
    search_fields = ('submissao_aceita__projeto__titulo_projeto',)