from django.db import models


class Usuario(models.Model):
    TIPOS = (
        (1, 'Aluno'),
        (2, 'Professor'),
        (3, 'Coordenador'),
    )

    nome_usuario = models.CharField(max_length=255)
    email_usuario = models.EmailField(unique=True)
    tipo_usuario = models.IntegerField(choices=TIPOS)
    ra = models.IntegerField(null=True, blank=True, verbose_name='RA')

    def __str__(self):
        return self.nome_usuario


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

    '''usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='projetos',
        limit_choices_to={'tipo_usuario': 1}
    )'''
    usuario = models.ForeignKey(
    Usuario,
    on_delete=models.CASCADE,
    related_name='projetos',
    limit_choices_to={'tipo_usuario': 1},
    null=True,  
    blank=True
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

    resultado_submissao = models.IntegerField(choices=RESULTADOS, default=0)
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='submissoes'
    )
    feedback = models.TextField(null=True, blank=True)
    data_submissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Submissão #{self.id} - {self.projeto.titulo_projeto}'


class Revista(models.Model):
    revista_publicada = models.CharField(max_length=255)
    semestre = models.ForeignKey(
        Semestre,
        on_delete=models.CASCADE,
        related_name='revistas'
    )

    def __str__(self):
        return self.revista_publicada


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
        verbose_name = 'Projeto por turma'
        verbose_name_plural = 'Projetos por turma'
        unique_together = ('projeto', 'turma', 'aluno')

    def __str__(self):
        return f'{self.aluno.nome_usuario} - {self.projeto.titulo_projeto} - {self.turma.nome_turma}'


class ProjetosSelecionados(models.Model):
    submissao_aceita = models.ForeignKey(
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
        verbose_name = 'Projeto selecionado'
        verbose_name_plural = 'Projetos selecionados'
        unique_together = ('submissao_aceita', 'revista')

    def __str__(self):
        return f'{self.submissao_aceita} -> {self.revista.revista_publicada}'