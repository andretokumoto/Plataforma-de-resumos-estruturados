from django.contrib import admin
from .models import CustomUser, Projeto, RevisaoProjeto, EdicaoRevista, EdicaoRevista_Projetos

# 1. Registrar o Usuário Customizado (sem customização, usa a forma direta)
admin.site.register(CustomUser)

# 2. Registrar o Modelo Principal do Projeto
@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo_projeto', 'id_autor', 'status_projeto', 'data_ultima_atualizacao')
    # O filtro de id_autor__email é um exemplo de como filtrar por campo em FK
    list_filter = ('status_projeto', 'programa_pepict', 'data_ultima_atualizacao')
    search_fields = ('titulo_projeto', 'id_autor__email')
    # Campos que você quer que o Admin veja em detalhes (opcional)
    # fieldsets = ( ... ) 
    
# 3. Registrar a Tabela de Revisão (AGORA SEM DUPLICIDADE)
# NOTA: O list_filter ('revisor__user_type') foi reintroduzido,
# mas SÓ vai funcionar corretamente se o erro E304 (conflito de users) foi corrigido antes em models.py
@admin.register(RevisaoProjeto)
class RevisaoProjetoAdmin(admin.ModelAdmin):
    list_display = ('projeto', 'revisor', 'status_revisao', 'data_revisao')
    llist_filter = ('status_revisao',)
    search_fields = ('projeto__titulo_projeto', 'revisor__email')

# 4. Registrar as Edições da Revista
@admin.register(EdicaoRevista)
class EdicaoRevistaAdmin(admin.ModelAdmin):
    list_display = ('titulo_revista', 'data_publicacao', 'arquivo_pdf')
    list_filter = ('data_publicacao',)
    
# 5. Registrar a Tabela de Ligação (Opcional, mas útil para ver os links)
admin.site.register(EdicaoRevista_Projetos)