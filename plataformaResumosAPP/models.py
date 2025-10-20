from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone



# 1. Tipos de Usuário (Para o Modelo Customizado de Usuário)
USER_TYPE_CHOICES = [
    ('AUTOR', 'Autor'),
    ('REVISOR', 'Revisor'),
    ('ADMIN', 'Administrador'),
]

# 2. Status do Projeto (Para o Modelo Projeto)
STATUS_CHOICES = [
    ('em_edicao', 'Em Edição'),
    ('submetido', 'Submetido para Revisão'),
    ('aprovado', 'Aprovado para Publicação'),
    ('rejeitado', 'Rejeitado / Requer Revisão'),
]

# 3. Status da Revisão (Para o Modelo RevisaoProjeto)
REVISAO_STATUS_CHOICES = [
    ('pendente', 'Pendente'),
    ('aprovado', 'Aprovado'),
    ('rejeitado', 'Rejeitado'),
]


# =====================================================================
# MODELO 1: USUÁRIO CUSTOMIZADO (Extensão do Django User)
# =====================================================================

class CustomUser(AbstractUser):

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set', # Novo nome para evitar o conflito
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions', # Novo nome para evitar o conflito
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    email = models.EmailField(unique=True, null=False, blank=False)
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='AUTOR',
        verbose_name="Tipo de Permissão"
    )

    # USERNAME_FIELD = 'email'  # Descomente se quiser usar o email para login
    # REQUIRED_FIELDS = ['username'] # Ajuste se USERNAME_FIELD for 'email'
    
    def __str__(self):
        return self.email

# OBS: Não se esqueça de adicionar AUTH_USER_MODEL = 'seu_app.CustomUser' no settings.py
# =====================================================================


# =====================================================================
# MODELOS DE DADOS DO PROJETO E REVISÃO
# =====================================================================

class Projeto(models.Model):
    """
    Armazena os dados de um projeto de extensão submetido.
    """
    # Chaves e Relacionamentos
    id_autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projetos_autorados',
        verbose_name="Autor Principal"
    )
    
    # Dados Estruturados (JSONB no PostgreSQL)
    nome_autores = models.JSONField(
        default=list,
        help_text="Lista de co-autores em formato JSON."
    )
    referencia_projeto = models.JSONField(
        default=list,
        help_text="Lista de referências bibliográficas em formato JSON/BibTeX."
    )
    
    # Campos de Metadados e Relatório
    titulo_projeto = models.CharField(max_length=255)
    programa_pepict = models.CharField(max_length=255, blank=True, null=True)
    ods_projeto = models.CharField(max_length=255, blank=True, null=True)
    
    # Campos Longos (TEXT)
    objetivos_trabalho = models.TextField()
    metodologia_projeto = models.TextField()
    resultados_projeto = models.TextField()
    reflexao_projeto = models.TextField()
    
    # Status e Datas
    status_projeto = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='em_edicao',
        verbose_name="Status de Publicação"
    )
    data_submissao = models.DateTimeField(null=True, blank=True)
    data_ultima_atualizacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo_projeto

class RevisaoProjeto(models.Model):
    """
    Gerencia o feedback e status de revisão de um projeto por um revisor específico.
    """
    projeto = models.ForeignKey(
        Projeto, 
        on_delete=models.CASCADE,
        related_name='avaliacoes'
    )
    revisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'REVISOR'}, # Limita a FK para revisores
        related_name='revisoes_realizadas'
    )
    
    status_revisao = models.CharField(
        max_length=20,
        choices=REVISAO_STATUS_CHOICES,
        default='pendente'
    )
    comentarios = models.TextField(blank=True, verbose_name="Comentários do Revisor")
    data_revisao = models.DateTimeField(null=True, blank=True)
    
    # Garante que um revisor só possa criar uma revisão por projeto
    class Meta:
        unique_together = ('projeto', 'revisor')

    def __str__(self):
        return f"Revisão de {self.projeto.titulo_projeto} por {self.revisor.email}"


# =====================================================================
# MODELOS DA REVISTA/LIVRO
# =====================================================================

class EdicaoRevista(models.Model):
    """
    Armazena os metadados de cada edição da revista publicada.
    """
    titulo_revista = models.CharField(max_length=255, unique=True)
    
    # O campo Many-to-Many é definido aqui, apontando para o modelo 'through'
    projetos = models.ManyToManyField(
        Projeto, 
        through='EdicaoRevista_Projetos', 
        related_name='edicoes_publicadas'
    )
    
    data_fechamento_submissoes = models.DateField(null=True, blank=True)
    data_publicacao = models.DateField(null=True, blank=True)
    arquivo_pdf = models.FileField(
        upload_to='revistas/pdfs/', 
        max_length=255,
        null=True,
        blank=True,
        verbose_name="PDF da Revista"
    )

    def __str__(self):
        return self.titulo_revista

class EdicaoRevista_Projetos(models.Model):
    """
    Tabela intermediária que define a ordem dos projetos em cada edição.
    """
    edicao = models.ForeignKey(EdicaoRevista, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    
    ordem_na_revista = models.IntegerField(default=1)

    class Meta:
        # Garante que um projeto só possa aparecer uma vez por edição
        unique_together = ('edicao', 'projeto') 
        ordering = ['edicao', 'ordem_na_revista']

    def __str__(self):
        return f"{self.projeto.titulo_projeto} na Edição {self.edicao.titulo_revista}"