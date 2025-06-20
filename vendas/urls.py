from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_vendas, name='dashboard'),
    
    # Orçamento URLs
    path('orcamentos/', views.OrcamentoListView.as_view(), name='orcamento_list'),
    path('orcamentos/novo/', views.OrcamentoCreateView.as_view(), name='orcamento_create'),
    path('orcamentos/<int:pk>/', views.OrcamentoDetailView.as_view(), name='orcamento_detail'),
    path('orcamentos/<int:pk>/editar/', views.OrcamentoUpdateView.as_view(), name='orcamento_update'),
    path('orcamentos/<int:pk>/excluir/', views.OrcamentoDeleteView.as_view(), name='orcamento_delete'),
    
    # Pedido de Venda URLs
    path('pedidos/', views.PedidoVendaListView.as_view(), name='pedido_list'),
    path('pedidos/novo/', views.PedidoVendaCreateView.as_view(), name='pedido_create'),
    path('pedidos/<int:pk>/', views.PedidoVendaDetailView.as_view(), name='pedido_detail'),
    path('pedidos/<int:pk>/editar/', views.PedidoVendaUpdateView.as_view(), name='pedido_update'),
    path('pedidos/<int:pk>/excluir/', views.PedidoVendaDeleteView.as_view(), name='pedido_delete'),
    
    # Comissão URLs
    path('comissoes/', views.ComissaoVendedorListView.as_view(), name='comissao_list'),
    path('comissoes/nova/', views.ComissaoVendedorCreateView.as_view(), name='comissao_create'),
    path('comissoes/<int:pk>/', views.ComissaoVendedorDetailView.as_view(), name='comissao_detail'),
    path('comissoes/<int:pk>/editar/', views.ComissaoVendedorUpdateView.as_view(), name='comissao_update'),
    
    # Meta de Vendedor URLs
    path('metas/', views.MetaVendedorListView.as_view(), name='meta_list'),
    path('metas/nova/', views.MetaVendedorCreateView.as_view(), name='meta_create'),
    path('metas/<int:pk>/editar/', views.MetaVendedorUpdateView.as_view(), name='meta_update'),
    
    # Relatórios URLs
    path('relatorios/vendas-vendedor/', views.relatorio_vendas_vendedor, name='relatorio_vendas_vendedor'),
    path('relatorios/produtos-mais-vendidos/', views.relatorio_produtos_mais_vendidos, name='relatorio_produtos_mais_vendidos'),
    
    # AJAX URLs
    path('ajax/converter-orcamento/<int:orcamento_id>/', views.converter_orcamento_pedido, name='converter_orcamento_pedido'),
    path('ajax/marcar-comissao-paga/<int:comissao_id>/', views.marcar_comissao_paga, name='marcar_comissao_paga'),
]

