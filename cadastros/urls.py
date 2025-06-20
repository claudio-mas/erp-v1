from django.urls import path
from . import views

app_name = 'cadastros'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_cadastros, name='dashboard'),
    
    # Cliente URLs
    path('clientes/', views.ClienteListView.as_view(), name='cliente_list'),
    path('clientes/novo/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/', views.ClienteDetailView.as_view(), name='cliente_detail'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/excluir/', views.ClienteDeleteView.as_view(), name='cliente_delete'),
    
    # Fornecedor URLs
    path('fornecedores/', views.FornecedorListView.as_view(), name='fornecedor_list'),
    path('fornecedores/novo/', views.FornecedorCreateView.as_view(), name='fornecedor_create'),
    path('fornecedores/<int:pk>/', views.FornecedorDetailView.as_view(), name='fornecedor_detail'),
    path('fornecedores/<int:pk>/editar/', views.FornecedorUpdateView.as_view(), name='fornecedor_update'),
    path('fornecedores/<int:pk>/excluir/', views.FornecedorDeleteView.as_view(), name='fornecedor_delete'),
    
    # Produto URLs
    path('produtos/', views.ProdutoListView.as_view(), name='produto_list'),
    path('produtos/novo/', views.ProdutoCreateView.as_view(), name='produto_create'),
    path('produtos/<int:pk>/', views.ProdutoDetailView.as_view(), name='produto_detail'),
    path('produtos/<int:pk>/editar/', views.ProdutoUpdateView.as_view(), name='produto_update'),
    path('produtos/<int:pk>/excluir/', views.ProdutoDeleteView.as_view(), name='produto_delete'),
    
    # Vendedor URLs
    path('vendedores/', views.VendedorListView.as_view(), name='vendedor_list'),
    path('vendedores/novo/', views.VendedorCreateView.as_view(), name='vendedor_create'),
    path('vendedores/<int:pk>/', views.VendedorDetailView.as_view(), name='vendedor_detail'),
    path('vendedores/<int:pk>/editar/', views.VendedorUpdateView.as_view(), name='vendedor_update'),
    path('vendedores/<int:pk>/excluir/', views.VendedorDeleteView.as_view(), name='vendedor_delete'),
    
    # Tabelas Auxiliares URLs
    path('estados/', views.EstadoListView.as_view(), name='estado_list'),
    path('estados/novo/', views.EstadoCreateView.as_view(), name='estado_create'),
    path('estados/<int:pk>/editar/', views.EstadoUpdateView.as_view(), name='estado_update'),
    
    path('cidades/', views.CidadeListView.as_view(), name='cidade_list'),
    path('cidades/novo/', views.CidadeCreateView.as_view(), name='cidade_create'),
    path('cidades/<int:pk>/editar/', views.CidadeUpdateView.as_view(), name='cidade_update'),
    
    # AJAX URLs
    path('ajax/cidades-por-estado/', views.buscar_cidades_por_estado, name='buscar_cidades_por_estado'),
    path('ajax/buscar-produtos/', views.buscar_produtos, name='buscar_produtos'),
    path('ajax/buscar-clientes/', views.buscar_clientes, name='buscar_clientes'),
    path('ajax/buscar-fornecedores/', views.buscar_fornecedores, name='buscar_fornecedores'),
]

