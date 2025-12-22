from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class CategoriaPrincipal(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordem', 'nome']
        verbose_name = 'Categoria Principal'
        verbose_name_plural = 'Categorias Principais'

    def __str__(self):
        return self.nome

class Subcategoria(models.Model):
    categoria_principal = models.ForeignKey(CategoriaPrincipal, on_delete=models.CASCADE, related_name='subcategorias')
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordem', 'nome']
        verbose_name = 'Subcategoria'
        verbose_name_plural = 'Subcategorias'
        unique_together = ['categoria_principal', 'nome']

    def __str__(self):
        return f"{self.categoria_principal.nome} - {self.nome}"

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descricao = models.TextField(blank=True)
    categoria_principal = models.ForeignKey(
        CategoriaPrincipal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Categoria principal"
    )
    categoria = models.CharField(max_length=100, blank=True, help_text="Subcategoria: Amadeirados, Tijolinho, Mosaicos, etc.")
    tag = models.CharField(max_length=100, default="Base Cementícia")
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    imagem_2 = models.ImageField(upload_to='produtos/', blank=True, null=True)
    imagem_3 = models.ImageField(upload_to='produtos/', blank=True, null=True)
    imagem_nome = models.CharField(max_length=200, blank=True, help_text="Nome do arquivo da imagem em static/images/")
    dimensoes = models.CharField(max_length=100, blank=True, help_text="Ex: 30x30x2cm")
    cor = models.CharField(max_length=100, blank=True, help_text="Ex: Cor natural (concreto cinza)")
    unidade_venda = models.CharField(max_length=100, blank=True, help_text="Ex: Vendido o M²")
    especificacoes = models.TextField(blank=True, help_text="Especificações adicionais, uma por linha")
    ativo = models.BooleanField(default=True)
    ordem = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordem', 'nome']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def save(self, *args, **kwargs):
        # Gerar slug automaticamente se não existir, estiver vazio, ou for inválido
        import re
        slug_pattern = re.compile(r'^[-a-zA-Z0-9_]+$')
        
        if not self.slug or not slug_pattern.match(self.slug) or (self.pk and Produto.objects.get(pk=self.pk).nome != self.nome):
            self.slug = slugify(self.nome)
            # Garantir que o slug seja único
            original_slug = self.slug
            counter = 1
            while Produto.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('produto-detalhe', kwargs={'slug': self.slug})
    
    def get_imagem_url(self):
        """Retorna a URL da imagem do produto"""
        # Retorna a primeira imagem disponível (ordem: imagem, imagem_2, imagem_3, imagem_nome)
        if self.imagem:
            try:
                return self.imagem.url
            except:
                pass
        if self.imagem_2:
            try:
                return self.imagem_2.url
            except:
                pass
        if self.imagem_3:
            try:
                return self.imagem_3.url
            except:
                pass
        if self.imagem_nome:
            # Garante que seja uma URL absoluta
            imagem_nome = self.imagem_nome.strip()
            if imagem_nome.startswith('http'):
                return imagem_nome
            elif imagem_nome.startswith('/static/'):
                return imagem_nome
            elif imagem_nome.startswith('static/'):
                return f'/{imagem_nome}'
            else:
                return f'/static/images/{imagem_nome}'
        return '/static/images/placeholder.png'  # Placeholder se nada funcionar

    def get_imagens_urls(self):
        """Retorna lista de URLs das imagens disponíveis (em ordem)."""
        urls = []
        if self.imagem:
            urls.append(self.imagem.url)
        if self.imagem_2:
            urls.append(self.imagem_2.url)
        if self.imagem_3:
            urls.append(self.imagem_3.url)
        if self.imagem_nome and not urls:
            # apenas adicionar imagem_nome se nenhuma ImageField estiver presente
            urls.append(f'/static/images/{self.imagem_nome}')
        return urls

class MensagemContato(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mensagem de Contato'
        verbose_name_plural = 'Mensagens de Contato'
    
    def __str__(self):
        return f"{self.nome} - {self.email} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"
