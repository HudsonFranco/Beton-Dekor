from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quem-somos/', views.quem_somos, name='quem-somos'),
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/<slug:slug>/', views.produto_detalhe, name='produto-detalhe'),
    path('contato/', views.contato, name='contato'),
    
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin - CRUD de Produtos
    path('admin/produtos/', views.admin_produtos, name='admin-produtos'),
    path('admin/produtos/criar/', views.admin_produto_create, name='admin-produto-create'),
    path('admin/produtos/<int:pk>/editar/', views.admin_produto_edit, name='admin-produto-edit'),
    path('admin/produtos/<int:pk>/duplicar/', views.admin_produto_duplicate, name='admin-produto-duplicate'),
    path('admin/produtos/<int:pk>/deletar/', views.admin_produto_delete, name='admin-produto-delete'),
    
    # Admin - CRUD de Categorias
    path('admin/categorias/', views.admin_categorias, name='admin-categorias'),
    path('admin/categorias/criar/', views.admin_categoria_create, name='admin-categoria-create'),
    path('admin/categorias/<int:pk>/editar/', views.admin_categoria_edit, name='admin-categoria-edit'),
    path('admin/categorias/<int:pk>/duplicar/', views.admin_categoria_duplicate, name='admin-categoria-duplicate'),
    path('admin/categorias/<int:pk>/deletar/', views.admin_categoria_delete, name='admin-categoria-delete'),
    
    # Admin - CRUD de Subcategorias
    path('admin/categorias/<int:categoria_pk>/subcategorias/criar/', views.admin_subcategoria_create, name='admin-subcategoria-create'),
    path('admin/subcategorias/<int:pk>/editar/', views.admin_subcategoria_edit, name='admin-subcategoria-edit'),
    path('admin/subcategorias/<int:pk>/deletar/', views.admin_subcategoria_delete, name='admin-subcategoria-delete'),
]

