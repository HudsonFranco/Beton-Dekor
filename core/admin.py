from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import Produto, CategoriaPrincipal, Subcategoria, MensagemContato


class ImageWithAddWidget(forms.ClearableFileInput):
        """Widget customizado que renderiza o input file padrão e adiciona
        um botão '+' inline para revelar os campos imagem_2 e imagem_3.
        Isso garante visibilidade do botão mesmo que JS estático não carregue."""
        template_name = 'django/forms/widgets/clearable_file_input.html'

        def render(self, name, value, attrs=None, renderer=None):
                input_html = super().render(name, value, attrs=attrs, renderer=renderer)
                # botão inline com handler que revela inputs por name
                btn = (
                        '<button type="button" id="add-image-btn-inline" class="button" '
                        'style="margin-left:8px;">+</button>'
                )

                script = '''
<script>
(function(){
    var btn = document.getElementById('add-image-btn-inline');
    if (!btn) return;
    btn.addEventListener('click', function(){
        var names = ['imagem_2','imagem_3'];
        for (var i=0;i<names.length;i++){
            var input = document.querySelector('[name="'+names[i]+'"]');
            if (input){
                // encontrar o container mais próximo e mostrar
                var row = input.closest('.form-row') || input.closest('.field-'+names[i]) || input.parentNode;
                if (row) row.style.display = '';
                // focus no input
                input.focus();
                return;
            }
        }
        // se nenhum encontrado, desabilitar
        btn.disabled = true;
    });
})();
</script>
'''

                return mark_safe(input_html + btn + script)

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
    
    # Use a custom ModelForm to inject a permanent + button beside the main image field
    class ProdutoAdminForm(forms.ModelForm):
        class Meta:
            model = Produto
            fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if 'imagem' in self.fields:
                # Use custom widget that renders the + button inline, to ensure
                # the UI is present regardless of theme or static JS availability.
                self.fields['imagem'].widget = ImageWithAddWidget()
                # Also keep/help_text if present
                if self.fields['imagem'].help_text:
                    self.fields['imagem'].help_text = self.fields['imagem'].help_text

    form = ProdutoAdminForm

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'slug', 'descricao', 'ativo', 'ordem')
        }),
        ('Categorização', {
            'fields': ('categoria_principal', 'categoria', 'tag')
        }),
        ('Imagem do Produto', {
                'fields': ('imagem', 'imagem_2', 'imagem_3', 'imagem_nome'),
            'description': 'Você pode fazer upload de uma imagem ou usar o nome de um arquivo existente em static/images/'
        }),
        ('Especificações do Produto', {
            'fields': ('dimensoes', 'cor', 'unidade_venda', 'especificacoes')
        }),
    )

    class Media:
        js = ('js/admin-produto-images.js',)

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
