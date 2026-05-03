from django.contrib import admin
from .models import (
    Usuario,
    Semestre,
    Programa,
    ODS,
    Turma,
    Inscricao,
    Projeto,
    Submissao,
    Revista,
    ProjetoRevista
)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'tipo_usuario',
        'is_staff',
    )
    list_filter = (
        'tipo_usuario',
        'is_staff',
    )
    search_fields = (
        'username',
        'email',
        'ra',
    )

@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = (
        'ano',
        'semestre',
        'coordenador',
    )
    list_filter = (
        'ano',
        'semestre',
    )

@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
    )
    search_fields = (
        'nome',
    )

@admin.register(ODS)
class ODSAdmin(admin.ModelAdmin):
    list_display = (
        'numero',
        'nome',
    )
    ordering = (
        'numero',
    )
    search_fields = (
        'nome',
    )

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = (
        'nome_turma',
        'disciplina',
        'curso',
        'semestre',
        'responsavel',
        'codigo_acesso',
    )
    list_filter = (
        'semestre',
        'curso',
        'disciplina',
    )
    search_fields = (
        'nome_turma',
        'disciplina',
        'codigo_acesso',
    )

@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = (
        'aluno',
        'turma',
        'data_inscricao',
    )
    list_filter = (
        'turma',
    )
    search_fields = (
        'aluno__username',
    )

class SubmissaoInline(admin.TabularInline):
    model = Submissao
    extra = 0
    readonly_fields = (
        'data_submissao',
    )

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo_projeto',
        'aluno',
        'turma',
        'exibir_programas',
        'status_projeto',
    )
    list_filter = (
        'status_projeto',
        'turma',
    )
    search_fields = (
        'titulo_projeto',
        'aluno__username',
    )
    filter_horizontal = (
        'ods',
        'programa',
    )
    inlines = [
        SubmissaoInline
    ]

    def exibir_programas(self, obj):
        return ", ".join([p.nome for p in obj.programa.all()])
    
    exibir_programas.short_description = 'Programas'

class ProjetoRevistaInline(admin.TabularInline):
    model = ProjetoRevista
    extra = 0

@admin.register(Revista)
class RevistaAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'semestre',
        'data_criacao',
    )
    list_filter = (
        'semestre',
    )
    inlines = [
        ProjetoRevistaInline
    ]

@admin.register(ProjetoRevista)
class ProjetoRevistaAdmin(admin.ModelAdmin):
    list_display = (
        'revista',
        'projeto',
    )
    list_filter = (
        'revista',
    )