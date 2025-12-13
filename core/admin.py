from django.contrib import admin
from .models import Produto, CategoriaPrincipal, Subcategoria, MensagemContato

@admin.register(CategoriaPrincipal)
class CategoriaPrincipalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ordem', 'ativo', 'created_at']
    list_filter = ['ativo']
    search_fields = ['nome']
    ordering = ['ordem', 'nome']

@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria_principal', 'ordem', 'ativo', 'created_at']
    list_filter = ['ativo', 'categoria_principal']
    search_fields = ['nome', 'categoria_principal__nome']
    ordering = ['categoria_principal__ordem', 'ordem', 'nome']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria_principal', 'categoria', 'ativo', 'ordem', 'created_at']
    list_filter = ['ativo', 'categoria_principal', 'categoria']
    search_fields = ['nome', 'categoria', 'categoria_principal', 'descricao']
    ordering = ['ordem', 'nome']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'slug', 'descricao', 'ativo', 'ordem')
        }),
        ('Categorização', {
            'fields': ('categoria_principal', 'categoria', 'tag')
        }),
        ('Imagem do Produto', {
            'fields': ('imagem', 'imagem_nome'),
            'description': 'Você pode fazer upload de uma imagem ou usar o nome de um arquivo existente em static/images/'
        }),
        ('Especificações do Produto', {
            'fields': ('dimensoes', 'cor', 'unidade_venda', 'especificacoes')
        }),
    )

@admin.register(MensagemContato)
class MensagemContatoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'lida', 'created_at']
    list_filter = ['lida', 'created_at']
    search_fields = ['nome', 'email', 'mensagem']
    readonly_fields = ['nome', 'email', 'mensagem', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informações do Contato', {
            'fields': ('nome', 'email', 'created_at')
        }),
        ('Mensagem', {
            'fields': ('mensagem',)
        }),
        ('Status', {
            'fields': ('lida',)
        }),
    )
