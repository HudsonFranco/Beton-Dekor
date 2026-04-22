from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from cloudinary import models as cloudinary_models

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
    subcategoria = models.ForeignKey(
        Subcategoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtos',
        help_text="Subcategoria associada (quando aplicável)"
    )
    categoria = models.CharField(max_length=100, blank=True, help_text="Subcategoria: Amadeirados, Tijolinho, Mosaicos, etc.")
    tag = models.CharField(max_length=100, default="Base Cementícia")
    imagem = cloudinary_models.CloudinaryField(folder='produtos/', blank=True, null=True)
    imagem_2 = cloudinary_models.CloudinaryField(folder='produtos/', blank=True, null=True)
    imagem_3 = cloudinary_models.CloudinaryField(folder='produtos/', blank=True, null=True)
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
        """Retorna a URL da imagem do produto (apenas para ImageField)"""
        if self.imagem:
            return self.imagem.url
        return None

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
            urls.append(f'{settings.STATIC_URL}images/{self.imagem_nome}')
        return urls

    @property
    def subcategoria_nome(self):
        """Retorna o nome da subcategoria (FK) ou o valor legado do campo `categoria`."""
        if self.subcategoria:
            return self.subcategoria.nome
        return self.categoria

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

class Destaque(models.Model):
    TIPO_CHOICES = (
        ('imagem', 'Imagem'),
        ('video', 'Vídeo'),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='imagem', verbose_name="Tipo de Mídia")
    titulo = models.CharField(max_length=200, blank=True, verbose_name="Título (ex: Revestimento em Tijolos)")
    subtitulo = models.CharField(max_length=200, blank=True, verbose_name="Subtítulo (ex: Perfeito para sua sala)")
    arquivo = cloudinary_models.CloudinaryField(
        resource_type='auto', 
        folder='destaques/', 
        blank=True, 
        null=True, 
        verbose_name="Arquivo (Foto ou Vídeo)"
    )
    produto_link = models.ForeignKey(
        'Produto', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Produto para 'Saiba Mais'"
    )
    link_externo = models.CharField(max_length=500, blank=True, verbose_name="Link Externo (caso não seja produto)")
    ordem = models.IntegerField(default=0, verbose_name="Ordem")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordem', 'created_at']
        verbose_name = 'Destaque'
        verbose_name_plural = 'Destaques'

    def save(self, *args, **kwargs):
        if self.arquivo:
            # Tenta detectar o tipo pelo nome do arquivo ou URL
            url = str(self.arquivo).lower()
            video_extensions = ['.mp4', '.mov', '.avi', '.m4v', 'video/upload']
            if any(ext in url for ext in video_extensions):
                self.tipo = 'video'
            else:
                self.tipo = 'imagem'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo or f"Slide {self.id}"
