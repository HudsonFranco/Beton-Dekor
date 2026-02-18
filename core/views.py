import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
from dotenv import load_dotenv
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
print("Carregando .env de:", dotenv_path)
load_dotenv(dotenv_path=dotenv_path, override=True)
print("BREVO_API_KEY do .env:", os.getenv("BREVO_API_KEY"))
print("BREVO_API_KEY from env:", os.getenv("BREVO_API_KEY"))
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_htmx.http import HttpResponseClientRedirect
from django.core.mail import send_mail
from .models import Produto, CategoriaPrincipal, Subcategoria, MensagemContato
import os

def home(request):
    return render(request, 'core/home.html')

def quem_somos(request):
    return render(request, 'core/quem-somos.html')

def produtos(request):
    categoria_filtro = request.GET.get('categoria', '').lower()
    
    # Buscar categorias principais do banco
    categorias_principais = CategoriaPrincipal.objects.filter(ativo=True).order_by('ordem', 'nome')
    
    # Agrupar produtos por categoria_principal - usar lista para facilitar no template
    produtos_agrupados_list = []
    for categoria in categorias_principais:
        produtos_categoria = Produto.objects.filter(
            ativo=True,
            categoria_principal=categoria
        ).order_by('ordem', 'nome')
        if produtos_categoria.exists():
            produtos_agrupados_list.append({
                'categoria': categoria,
                'produtos': produtos_categoria
            })
    
    # Também criar dicionário para compatibilidade
    produtos_agrupados = {}
    for item in produtos_agrupados_list:
        produtos_agrupados[item['categoria'].nome] = item['produtos']
    
    # SEMPRE retornar TODOS os produtos ativos
    # O filtro será aplicado via JavaScript no frontend
    produtos_list = Produto.objects.filter(ativo=True).order_by('ordem', 'nome')
    
    return render(request, 'core/produtos.html', {
        'produtos': produtos_list,
        'produtos_agrupados': produtos_agrupados,
        'produtos_agrupados_list': produtos_agrupados_list,  # Nova estrutura mais fácil de usar
        'categoria_filtro': categoria_filtro,
        'categorias_principais': categorias_principais
    })

def produto_detalhe(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    outros_produtos = Produto.objects.exclude(slug=slug).filter(ativo=True).order_by('ordem', 'nome')[:4]
    return render(request, 'core/produto-detalhe.html', {
        'produto': produto,
        'outros_produtos': outros_produtos
    })

def contato(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        mensagem = request.POST.get('mensagem', '').strip()
        
        # Validar campos
        if nome and email and mensagem:
            # Salvar mensagem no banco de dados
            MensagemContato.objects.create(
                nome=nome,
                email=email,
                mensagem=mensagem
            )

            # Enviar e-mail via SMTP
            try:
                send_mail(
                    subject=f'Nova mensagem de contato - {nome}',
                    message=f'Nome: {nome}\nE-mail: {email}\nMensagem:\n{mensagem}',
                    from_email='betondekor@outlook.com',
                    recipient_list=[os.getenv('BREVO_TEST_EMAIL', 'hudsonfranco17@gmail.com')],
                    fail_silently=False,
                )
                print('Email enviado com sucesso via SMTP')
            except Exception as e:
                print(f'Erro ao enviar email: {e}')
            
            if request.htmx:
                # Retorna uma mensagem de sucesso via HTMX
                return render(request, 'core/contact_success.html', {
                    'nome': nome
                })
            else:
                messages.success(request, 'Mensagem enviada com sucesso!')
                return redirect('home')
        else:
            if request.htmx:
                return render(request, 'core/contact_success.html', {
                    'nome': nome,
                    'erro': 'Por favor, preencha todos os campos.'
                })
            else:
                messages.error(request, 'Por favor, preencha todos os campos.')
                return redirect('contato')
    
    return render(request, 'core/contato.html')

# Autenticação
def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin-produtos')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('admin-produtos')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    return render(request, 'core/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('home')

# Admin - CRUD de Produtos
@login_required
def admin_produtos(request):
    produtos_list = Produto.objects.all()
    categorias = CategoriaPrincipal.objects.filter(ativo=True).prefetch_related('subcategorias')
    return render(request, 'core/admin/produtos_list.html', {
        'produtos': produtos_list,
        'categorias': categorias
    })

@login_required
def admin_produto_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        slug = request.POST.get('slug')
        descricao = request.POST.get('descricao', '')
        categoria_principal_id = request.POST.get('categoria_principal', '')
        categoria = request.POST.get('categoria', '')
        tag = request.POST.get('tag', 'Base Cementícia')
        imagem_nome = request.POST.get('imagem_nome', '')
        ordem = request.POST.get('ordem', 0)
        ativo = request.POST.get('ativo') == 'on'

        categoria_principal = None
        if categoria_principal_id:
            try:
                categoria_principal = CategoriaPrincipal.objects.get(pk=categoria_principal_id)
            except CategoriaPrincipal.DoesNotExist:
                pass

        produto = Produto(
            nome=nome,
            slug=slug if slug else None,  # Será gerado automaticamente no save() se vazio
            descricao=descricao,
            categoria_principal=categoria_principal,
            categoria=categoria,
            subcategoria=None,
            tag=tag,
            imagem_nome=imagem_nome,
            dimensoes=request.POST.get('dimensoes', ''),
            cor=request.POST.get('cor', ''),
            unidade_venda=request.POST.get('unidade_venda', ''),
            especificacoes=request.POST.get('especificacoes', ''),
            ordem=int(ordem) if ordem else 0,
            ativo=ativo
        )
        
        # Processar upload de imagens
        if 'imagem' in request.FILES:
            produto.imagem = request.FILES['imagem']
        if 'imagem_2' in request.FILES:
            produto.imagem_2 = request.FILES['imagem_2']
        if 'imagem_3' in request.FILES:
            produto.imagem_3 = request.FILES['imagem_3']
        
        produto.save()  # Isso vai gerar o slug automaticamente se não foi fornecido
        # associar subcategoria se enviada
        subcategoria_id = request.POST.get('subcategoria')
        if subcategoria_id:
            try:
                produto.subcategoria = Subcategoria.objects.get(pk=subcategoria_id)
                produto.save()
            except Subcategoria.DoesNotExist:
                pass
        messages.success(request, f'Produto "{produto.nome}" criado com sucesso!')
        return redirect('admin-produtos')
    categorias_principais = CategoriaPrincipal.objects.filter(ativo=True).order_by('ordem', 'nome')
    return render(request, 'core/admin/produto_form.html', {'produto': None, 'categorias_principais': categorias_principais})

@login_required
def admin_produto_edit(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.nome = request.POST.get('nome')
        produto.slug = request.POST.get('slug')
        produto.descricao = request.POST.get('descricao', '')
        categoria_principal_id = request.POST.get('categoria_principal', '')
        categoria_principal = None
        if categoria_principal_id:
            try:
                categoria_principal = CategoriaPrincipal.objects.get(pk=categoria_principal_id)
            except CategoriaPrincipal.DoesNotExist:
                pass
        produto.categoria_principal = categoria_principal
        produto.categoria = request.POST.get('categoria', '')
        # Atualizar subcategoria (FK)
        subcategoria_id = request.POST.get('subcategoria', '')
        if subcategoria_id:
            try:
                produto.subcategoria = Subcategoria.objects.get(pk=subcategoria_id)
            except Subcategoria.DoesNotExist:
                produto.subcategoria = None
        else:
            produto.subcategoria = None
        produto.tag = request.POST.get('tag', 'Base Cementícia')
        produto.imagem_nome = request.POST.get('imagem_nome', '')
        produto.dimensoes = request.POST.get('dimensoes', '')
        produto.cor = request.POST.get('cor', '')
        produto.unidade_venda = request.POST.get('unidade_venda', '')
        produto.especificacoes = request.POST.get('especificacoes', '')
        produto.ordem = int(request.POST.get('ordem', 0)) if request.POST.get('ordem') else 0
        produto.ativo = request.POST.get('ativo') == 'on'
        
        # Processar upload de imagens (se novas imagens foram enviadas)
        if 'imagem' in request.FILES:
            produto.imagem = request.FILES['imagem']
        if 'imagem_2' in request.FILES:
            produto.imagem_2 = request.FILES['imagem_2']
        if 'imagem_3' in request.FILES:
            produto.imagem_3 = request.FILES['imagem_3']

        # Remover imagens existentes se o checkbox correspondente foi marcado
        if request.POST.get('remove_imagem') == 'on':
            try:
                if produto.imagem:
                    produto.imagem.delete(save=False)
            except Exception:
                pass
            produto.imagem = None
        if request.POST.get('remove_imagem_2') == 'on':
            try:
                if getattr(produto, 'imagem_2', None):
                    produto.imagem_2.delete(save=False)
            except Exception:
                pass
            produto.imagem_2 = None
        if request.POST.get('remove_imagem_3') == 'on':
            try:
                if getattr(produto, 'imagem_3', None):
                    produto.imagem_3.delete(save=False)
            except Exception:
                pass
            produto.imagem_3 = None
        
        produto.save()
        messages.success(request, f'Produto "{produto.nome}" atualizado com sucesso!')
        return redirect('admin-produtos')
    categorias_principais = CategoriaPrincipal.objects.filter(ativo=True).order_by('ordem', 'nome')
    return render(request, 'core/admin/produto_form.html', {'produto': produto, 'categorias_principais': categorias_principais})

@login_required
def admin_produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        nome = produto.nome
        produto.delete()
        messages.success(request, f'Produto "{nome}" deletado com sucesso!')
        return redirect('admin-produtos')
    return render(request, 'core/admin/produto_confirm_delete.html', {'produto': produto})

@login_required
def admin_produto_duplicate(request, pk):
    produto_original = get_object_or_404(Produto, pk=pk)
    
    # Criar novo produto baseado no original
    novo_produto = Produto(
        nome=f"{produto_original.nome} (Cópia)",
        slug=None,  # Será gerado automaticamente
        descricao=produto_original.descricao,
        categoria_principal=produto_original.categoria_principal,
        categoria=produto_original.categoria,
        tag=produto_original.tag,
        imagem_nome=produto_original.imagem_nome,
        dimensoes=produto_original.dimensoes,
        cor=produto_original.cor,
        unidade_venda=produto_original.unidade_venda,
        especificacoes=produto_original.especificacoes,
        ativo=produto_original.ativo,
        ordem=produto_original.ordem
    )
    
    # Copiar imagem se existir
    if produto_original.imagem:
        novo_produto.imagem = produto_original.imagem
    if getattr(produto_original, 'imagem_2', None):
        novo_produto.imagem_2 = produto_original.imagem_2
    if getattr(produto_original, 'imagem_3', None):
        novo_produto.imagem_3 = produto_original.imagem_3
    
    # Salvar (o slug será gerado automaticamente)
    novo_produto.save()
    
    messages.success(request, f'Produto "{novo_produto.nome}" duplicado com sucesso!')
    return redirect('admin-produtos')

# Admin - CRUD de Categorias
@login_required
def admin_categorias(request):
    categorias = CategoriaPrincipal.objects.all().prefetch_related('subcategorias')
    return render(request, 'core/admin/categorias_list.html', {'categorias': categorias})

@login_required
def admin_categoria_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        ordem = request.POST.get('ordem', 0)
        ativo = request.POST.get('ativo') == 'on'
        
        if nome:
            categoria = CategoriaPrincipal(
                nome=nome,
                ordem=int(ordem) if ordem else 0,
                ativo=ativo
            )
            categoria.save()
            messages.success(request, f'Categoria "{categoria.nome}" criada com sucesso!')
            return redirect('admin-produtos')
        else:
            messages.error(request, 'O nome da categoria é obrigatório.')
    
    return render(request, 'core/admin/categoria_form.html', {'categoria': None})

@login_required
def admin_categoria_edit(request, pk):
    categoria = get_object_or_404(CategoriaPrincipal, pk=pk)
    if request.method == 'POST':
        categoria.nome = request.POST.get('nome', '').strip()
        categoria.ordem = int(request.POST.get('ordem', 0)) if request.POST.get('ordem') else 0
        categoria.ativo = request.POST.get('ativo') == 'on'
        categoria.save()
        messages.success(request, f'Categoria "{categoria.nome}" atualizada com sucesso!')
        return redirect('admin-produtos')
    return render(request, 'core/admin/categoria_form.html', {'categoria': categoria})

@login_required
def admin_categoria_delete(request, pk):
    categoria = get_object_or_404(CategoriaPrincipal, pk=pk)
    if request.method == 'POST':
        nome = categoria.nome
        
        # Deletar todos os produtos associados à categoria
        produtos_associados = Produto.objects.filter(
            categoria_principal=categoria
        )
        quantidade_produtos = produtos_associados.count()
        produtos_associados.delete()
        
        # Deletar a categoria
        categoria.delete()
        
        if quantidade_produtos > 0:
            messages.success(request, f'Categoria "{nome}" e {quantidade_produtos} produto(s) associado(s) deletados com sucesso!')
        else:
            messages.success(request, f'Categoria "{nome}" deletada com sucesso!')
        
        return redirect('admin-produtos')
    
    # Contar produtos associados para mostrar no template de confirmação
    produtos_associados = Produto.objects.filter(
        categoria_principal=categoria
    )
    quantidade_produtos = produtos_associados.count()
    
    return render(request, 'core/admin/categoria_confirm_delete.html', {
        'categoria': categoria,
        'quantidade_produtos': quantidade_produtos
    })

@login_required
def admin_categoria_duplicate(request, pk):
    categoria_original = get_object_or_404(CategoriaPrincipal, pk=pk)
    
    # Criar nova categoria baseada na original
    nova_categoria = CategoriaPrincipal(
        nome=f"{categoria_original.nome} (Cópia)",
        ordem=categoria_original.ordem,
        ativo=categoria_original.ativo
    )
    
    nova_categoria.save()
    
    # Duplicar todos os produtos associados à categoria original
    # Buscar produtos que tenham categoria_principal igual ao nome da categoria original
    produtos_originais = Produto.objects.filter(
        categoria_principal=categoria_original
    )
    
    produtos_duplicados = 0
    for produto_original in produtos_originais:
        # Criar novo produto com nome único
        nome_base = produto_original.nome.replace(' (Cópia)', '')
        nome_novo = f"{nome_base} (Cópia)"
        
        # Garantir que o nome seja único
        counter = 1
        while Produto.objects.filter(nome=nome_novo).exists():
            nome_novo = f"{nome_base} (Cópia {counter})"
            counter += 1
        
        novo_produto = Produto(
            nome=nome_novo,
            slug=None,  # Será gerado automaticamente
            descricao=produto_original.descricao,
            categoria_principal=nova_categoria,  # Associar à nova categoria
            categoria=produto_original.categoria,
            tag=produto_original.tag,
            imagem_nome=produto_original.imagem_nome,
            dimensoes=produto_original.dimensoes,
            cor=produto_original.cor,
            unidade_venda=produto_original.unidade_venda,
            especificacoes=produto_original.especificacoes,
            ativo=produto_original.ativo,
            ordem=produto_original.ordem
        )
        
        # Copiar imagem se existir
        if produto_original.imagem:
            novo_produto.imagem = produto_original.imagem
        
        novo_produto.save()
        produtos_duplicados += 1
    
    if produtos_duplicados > 0:
        messages.success(request, f'Categoria "{nova_categoria.nome}" e {produtos_duplicados} produto(s) duplicados com sucesso!')
    else:
        messages.success(request, f'Categoria "{nova_categoria.nome}" duplicada com sucesso! (Nenhum produto encontrado na categoria original)')
    
    return redirect('admin-produtos')

# Admin - CRUD de Subcategorias
@login_required
def admin_subcategoria_create(request, categoria_pk):
    categoria = get_object_or_404(CategoriaPrincipal, pk=categoria_pk)
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        ordem = request.POST.get('ordem', 0)
        ativo = request.POST.get('ativo') == 'on'
        
        if nome:
            subcategoria = Subcategoria(
                categoria_principal=categoria,
                nome=nome,
                ordem=int(ordem) if ordem else 0,
                ativo=ativo
            )
            subcategoria.save()
            messages.success(request, f'Subcategoria "{subcategoria.nome}" criada com sucesso!')
            return redirect('admin-produtos')
        else:
            messages.error(request, 'O nome da subcategoria é obrigatório.')
    
    return render(request, 'core/admin/subcategoria_form.html', {'categoria': categoria, 'subcategoria': None})

@login_required
def admin_subcategoria_edit(request, pk):
    subcategoria = get_object_or_404(Subcategoria, pk=pk)
    if request.method == 'POST':
        subcategoria.nome = request.POST.get('nome', '').strip()
        subcategoria.categoria_principal_id = request.POST.get('categoria_principal')
        subcategoria.ordem = int(request.POST.get('ordem', 0)) if request.POST.get('ordem') else 0
        subcategoria.ativo = request.POST.get('ativo') == 'on'
        subcategoria.save()
        messages.success(request, f'Subcategoria "{subcategoria.nome}" atualizada com sucesso!')
        return redirect('admin-produtos')
    categorias_list = CategoriaPrincipal.objects.all()
    return render(request, 'core/admin/subcategoria_form.html', {
        'categoria': subcategoria.categoria_principal, 
        'subcategoria': subcategoria,
        'categoria_list': categorias_list
    })