from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_estoque, name='dashboard'),
    
    # Movimentação de Estoque URLs
    path('movimentacoes/', views.MovimentacaoEstoqueListView.as_view(), name='movimentacao_list'),
    path('movimentacoes/nova/', views.MovimentacaoEstoqueCreateView.as_view(), name='movimentacao_create'),
    path('movimentacoes/<int:pk>/', views.MovimentacaoEstoqueDetailView.as_view(), name='movimentacao_detail'),
    
    # Estoque de Produtos URLs
    path('estoque-produtos/', views.EstoqueProdutoListView.as_view(), name='estoque_produto_list'),
    path('estoque-produtos/<int:pk>/', views.EstoqueProdutoDetailView.as_view(), name='estoque_produto_detail'),
    
    # Inventário URLs
    path('inventarios/', views.InventarioListView.as_view(), name='inventario_list'),
    path('inventarios/novo/', views.InventarioCreateView.as_view(), name='inventario_create'),
    path('inventarios/<int:pk>/', views.InventarioDetailView.as_view(), name='inventario_detail'),
    path('inventarios/<int:pk>/editar/', views.InventarioUpdateView.as_view(), name='inventario_update'),
    
    # Reserva de Produto URLs
    path('reservas/', views.ReservaProdutoListView.as_view(), name='reserva_list'),
    path('reservas/nova/', views.ReservaProdutoCreateView.as_view(), name='reserva_create'),
    path('reservas/<int:pk>/', views.ReservaProdutoDetailView.as_view(), name='reserva_detail'),
    
    # Produto x Fornecedor URLs
    path('produto-fornecedor/', views.ProdutoFornecedorListView.as_view(), name='produto_fornecedor_list'),
    path('produto-fornecedor/novo/', views.ProdutoFornecedorCreateView.as_view(), name='produto_fornecedor_create'),
    path('produto-fornecedor/<int:pk>/editar/', views.ProdutoFornecedorUpdateView.as_view(), name='produto_fornecedor_update'),
    
    # Relatórios URLs
    path('relatorios/estoque-baixo/', views.relatorio_estoque_baixo, name='relatorio_estoque_baixo'),
    path('relatorios/movimentacoes-periodo/', views.relatorio_movimentacoes_periodo, name='relatorio_movimentacoes_periodo'),
    path('relatorios/inventario/<int:inventario_id>/', views.relatorio_inventario, name='relatorio_inventario'),
    
    # AJAX URLs
    path('ajax/liberar-reserva/<int:reserva_id>/', views.liberar_reserva, name='liberar_reserva'),
    path('ajax/ajustar-estoque/<int:item_id>/', views.ajustar_estoque_inventario, name='ajustar_estoque_inventario'),
    path('ajax/buscar-estoque-produto/', views.buscar_estoque_produto, name='buscar_estoque_produto'),
]

