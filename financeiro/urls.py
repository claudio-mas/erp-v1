from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_financeiro, name='dashboard'),
    
    # Plano de Contas URLs
    path('plano-contas/', views.PlanoContasListView.as_view(), name='plano_contas_list'),
    path('plano-contas/novo/', views.PlanoContasCreateView.as_view(), name='plano_contas_create'),
    path('plano-contas/<int:pk>/editar/', views.PlanoContasUpdateView.as_view(), name='plano_contas_update'),
    
    # Centro de Custo URLs
    path('centros-custo/', views.CentroCustoListView.as_view(), name='centro_custo_list'),
    path('centros-custo/novo/', views.CentroCustoCreateView.as_view(), name='centro_custo_create'),
    path('centros-custo/<int:pk>/editar/', views.CentroCustoUpdateView.as_view(), name='centro_custo_update'),
    
    # Contas a Pagar URLs
    path('contas-pagar/', views.ContasPagarListView.as_view(), name='contas_pagar_list'),
    path('contas-pagar/nova/', views.ContasPagarCreateView.as_view(), name='contas_pagar_create'),
    path('contas-pagar/<int:pk>/', views.ContasPagarDetailView.as_view(), name='contas_pagar_detail'),
    path('contas-pagar/<int:pk>/editar/', views.ContasPagarUpdateView.as_view(), name='contas_pagar_update'),
    
    # Contas a Receber URLs
    path('contas-receber/', views.ContasReceberListView.as_view(), name='contas_receber_list'),
    path('contas-receber/nova/', views.ContasReceberCreateView.as_view(), name='contas_receber_create'),
    path('contas-receber/<int:pk>/', views.ContasReceberDetailView.as_view(), name='contas_receber_detail'),
    path('contas-receber/<int:pk>/editar/', views.ContasReceberUpdateView.as_view(), name='contas_receber_update'),
    
    # Fluxo de Caixa URLs
    path('fluxo-caixa/', views.FluxoCaixaListView.as_view(), name='fluxo_caixa_list'),
    path('fluxo-caixa/novo/', views.FluxoCaixaCreateView.as_view(), name='fluxo_caixa_create'),
    
    # DRE URLs
    path('dre/', views.DREListView.as_view(), name='dre_list'),
    path('dre/nova/', views.DRECreateView.as_view(), name='dre_create'),
    path('dre/<int:pk>/', views.DREDetailView.as_view(), name='dre_detail'),
    path('dre/<int:pk>/editar/', views.DREUpdateView.as_view(), name='dre_update'),
    
    # Relatórios URLs
    path('relatorios/contas-pagar-vencer/', views.relatorio_contas_pagar_vencer, name='relatorio_contas_pagar_vencer'),
    path('relatorios/contas-receber-vencer/', views.relatorio_contas_receber_vencer, name='relatorio_contas_receber_vencer'),
    path('relatorios/fluxo-caixa-periodo/', views.relatorio_fluxo_caixa_periodo, name='relatorio_fluxo_caixa_periodo'),
    
    # AJAX URLs
    path('ajax/pagar-conta/<int:conta_id>/', views.pagar_conta, name='pagar_conta'),
    path('ajax/receber-conta/<int:conta_id>/', views.receber_conta, name='receber_conta'),
]

