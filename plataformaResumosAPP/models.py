from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):

    ALUNO = 1
    PROFESSOR = 2
    COORDENADOR = 3

    TIPOS = (
        (ALUNO, 'Aluno'),
        (PROFESSOR, 'Professor'),
        (COORDENADOR, 'Coordenador'),
    )

    tipo_usuario = models.IntegerField(
        choices=TIPOS,
        default=ALUNO
    )

    ra = models.IntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username


class Semestre(models.Model):
    ano = models.CharField(max_length=4)
    semestre = models.IntegerField()

    coordenador = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='semestres_coordenados',
        limit_choices_to={'tipo_usuario': 3}
    )

    def __str__(self):
        return f'{self.ano}/{self.semestre}'


class Turma(models.Model):
    responsavel = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='turmas_responsavel',
        limit_choices_to={'tipo_usuario': 2}
    )

    codigo_acesso = models.CharField(max_length=20, unique=True)
    nome_turma = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_turma


class Projeto(models.Model):
    STATUS = (
        (0, 'Rascunho'),
        (1, 'Em análise'),
        (2, 'Aprovado'),
        (3, 'Rejeitado'),
    )

    aluno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='projetos',
        limit_choices_to={'tipo_usuario': 1}
    )

    professor_responsavel = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='projetos_orientados',
        limit_choices_to={'tipo_usuario': 2}
    )

    titulo_projeto = models.CharField(max_length=255)
    nome_autores = models.TextField()
    programa_pepict = models.CharField(max_length=255)

    objetivos_trabalho = models.TextField()
    metodologia_projeto = models.TextField()
    resultados_projeto = models.TextField()
    ods_projeto = models.CharField(max_length=255)
    reflexao_projeto = models.TextField()
    referencia_projeto = models.TextField()

    status_projeto = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.titulo_projeto


class Submissao(models.Model):
    RESULTADOS = (
        (0, 'Em análise'),
        (1, 'Aprovado'),
        (2, 'Rejeitado'),
    )

    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='submissoes'
    )

    resultado_submissao = models.IntegerField(choices=RESULTADOS, default=0)
    feedback = models.TextField(null=True, blank=True)

    data_submissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Submissão #{self.id} - {self.projeto.titulo_projeto}'


class Revista(models.Model):
    titulo = models.CharField(max_length=255)

    semestre = models.ForeignKey(
        Semestre,
        on_delete=models.CASCADE,
        related_name='revistas'
    )

    def __str__(self):
        return self.titulo


class ProjetoPorTurma(models.Model):
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='vinculos_turma'
    )

    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='projetos_turma'
    )

    aluno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='projetos_em_turma',
        limit_choices_to={'tipo_usuario': 1}
    )

    class Meta:
        unique_together = ('projeto', 'turma', 'aluno')
        verbose_name = 'Projeto por turma'
        verbose_name_plural = 'Projetos por turma'

    def __str__(self):
        return f'{self.aluno.username} - {self.projeto.titulo_projeto} - {self.turma.nome_turma}'


class ProjetosSelecionados(models.Model):
    submissao = models.ForeignKey(
        Submissao,
        on_delete=models.CASCADE,
        related_name='selecoes_revista'
    )

    revista = models.ForeignKey(
        Revista,
        on_delete=models.CASCADE,
        related_name='projetos_selecionados'
    )

    class Meta:
        unique_together = ('submissao', 'revista')
        verbose_name = 'Projeto selecionado'
        verbose_name_plural = 'Projetos selecionados'

    def __str__(self):
        return f'{self.submissao} -> {self.revista.titulo}'