from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum
from django.http import JsonResponse
from datetime import datetime, date
from .models import (
    Orcamento, ItemOrcamento, PedidoVenda, ItemPedidoVenda,
    ComissaoVendedor, MetaVendedor, StatusOrcamento, StatusPedido
)
from .forms import (
    OrcamentoForm, ItemOrcamentoForm, PedidoVendaForm, ItemPedidoVendaForm,
    ComissaoVendedorForm, MetaVendedorForm
)
from cadastros.models import Cliente, Produto, Vendedor


@login_required
def dashboard_vendas(request):
    """Dashboard do módulo de vendas"""
    hoje = date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    # Estatísticas do mês atual
    orcamentos_mes = Orcamento.objects.filter(
        data_orcamento__month=mes_atual,
        data_orcamento__year=ano_atual
    )
    
    pedidos_mes = PedidoVenda.objects.filter(
        data_pedido__month=mes_atual,
        data_pedido__year=ano_atual
    )
    
    context = {
        'total_orcamentos_mes': orcamentos_mes.count(),
        'valor_orcamentos_mes': orcamentos_mes.aggregate(Sum('valor_total'))['valor_total__sum'] or 0,
        'total_pedidos_mes': pedidos_mes.count(),
        'valor_pedidos_mes': pedidos_mes.aggregate(Sum('valor_total'))['valor_total__sum'] or 0,
        'orcamentos_pendentes': Orcamento.objects.filter(status__codigo='PENDENTE').count(),
        'pedidos_abertos': PedidoVenda.objects.filter(status__codigo='ABERTO').count(),
    }
    return render(request, 'vendas/dashboard.html', context)


# Views para Orçamento
class OrcamentoListView(LoginRequiredMixin, ListView):
    model = Orcamento
    template_name = 'vendas/orcamento_list.html'
    context_object_name = 'orcamentos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Orcamento.objects.all()
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        vendedor = self.request.GET.get('vendedor')
        
        if search:
            queryset = queryset.filter(
                Q(numero__icontains=search) |
                Q(cliente__nome_razao_social__icontains=search)
            )
        
        if status:
            queryset = queryset.filter(status_id=status)
            
        if vendedor:
            queryset = queryset.filter(vendedor_id=vendedor)
            
        return queryset.order_by('-data_orcamento')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_list'] = StatusOrcamento.objects.filter(ativo=True)
        context['vendedores'] = Vendedor.objects.filter(ativo=True)
        return context


class OrcamentoDetailView(LoginRequiredMixin, DetailView):
    model = Orcamento
    template_name = 'vendas/orcamento_detail.html'
    context_object_name = 'orcamento'


class OrcamentoCreateView(LoginRequiredMixin, CreateView):
    model = Orcamento
    form_class = OrcamentoForm
    template_name = 'vendas/orcamento_form.html'
    success_url = reverse_lazy('vendas:orcamento_list')
    
    def form_valid(self, form):
        form.instance.usuario_criacao = self.request.user
        messages.success(self.request, 'Orçamento criado com sucesso!')
        return super().form_valid(form)


class OrcamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Orcamento
    form_class = OrcamentoForm
    template_name = 'vendas/orcamento_form.html'
    success_url = reverse_lazy('vendas:orcamento_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Orçamento atualizado com sucesso!')
        return super().form_valid(form)


class OrcamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Orcamento
    template_name = 'vendas/orcamento_confirm_delete.html'
    success_url = reverse_lazy('vendas:orcamento_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Orçamento excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# Views para Pedido de Venda
class PedidoVendaListView(LoginRequiredMixin, ListView):
    model = PedidoVenda
    template_name = 'vendas/pedido_list.html'
    context_object_name = 'pedidos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = PedidoVenda.objects.all()
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        vendedor = self.request.GET.get('vendedor')
        
        if search:
            queryset = queryset.filter(
                Q(numero__icontains=search) |
                Q(cliente__nome_razao_social__icontains=search)
            )
        
        if status:
            queryset = queryset.filter(status_id=status)
            
        if vendedor:
            queryset = queryset.filter(vendedor_id=vendedor)
            
        return queryset.order_by('-data_pedido')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_list'] = StatusPedido.objects.filter(ativo=True)
        context['vendedores'] = Vendedor.objects.filter(ativo=True)
        return context


class PedidoVendaDetailView(LoginRequiredMixin, DetailView):
    model = PedidoVenda
    template_name = 'vendas/pedido_detail.html'
    context_object_name = 'pedido'


class PedidoVendaCreateView(LoginRequiredMixin, CreateView):
    model = PedidoVenda
    form_class = PedidoVendaForm
    template_name = 'vendas/pedido_form.html'
    success_url = reverse_lazy('vendas:pedido_list')
    
    def form_valid(self, form):
        form.instance.usuario_criacao = self.request.user
        messages.success(self.request, 'Pedido de venda criado com sucesso!')
        return super().form_valid(form)


class PedidoVendaUpdateView(LoginRequiredMixin, UpdateView):
    model = PedidoVenda
    form_class = PedidoVendaForm
    template_name = 'vendas/pedido_form.html'
    success_url = reverse_lazy('vendas:pedido_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Pedido de venda atualizado com sucesso!')
        return super().form_valid(form)


class PedidoVendaDeleteView(LoginRequiredMixin, DeleteView):
    model = PedidoVenda
    template_name = 'vendas/pedido_confirm_delete.html'
    success_url = reverse_lazy('vendas:pedido_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Pedido de venda excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# Views para Comissão
class ComissaoVendedorListView(LoginRequiredMixin, ListView):
    model = ComissaoVendedor
    template_name = 'vendas/comissao_list.html'
    context_object_name = 'comissoes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ComissaoVendedor.objects.all()
        vendedor = self.request.GET.get('vendedor')
        pago = self.request.GET.get('pago')
        
        if vendedor:
            queryset = queryset.filter(vendedor_id=vendedor)
            
        if pago:
            queryset = queryset.filter(pago=(pago == 'true'))
            
        return queryset.order_by('-data_vencimento')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendedores'] = Vendedor.objects.filter(ativo=True)
        return context


class ComissaoVendedorDetailView(LoginRequiredMixin, DetailView):
    model = ComissaoVendedor
    template_name = 'vendas/comissao_detail.html'
    context_object_name = 'comissao'


class ComissaoVendedorCreateView(LoginRequiredMixin, CreateView):
    model = ComissaoVendedor
    form_class = ComissaoVendedorForm
    template_name = 'vendas/comissao_form.html'
    success_url = reverse_lazy('vendas:comissao_list')
    
    def form_valid(self, form):
        form.instance.usuario_criacao = self.request.user
        messages.success(self.request, 'Comissão criada com sucesso!')
        return super().form_valid(form)


class ComissaoVendedorUpdateView(LoginRequiredMixin, UpdateView):
    model = ComissaoVendedor
    form_class = ComissaoVendedorForm
    template_name = 'vendas/comissao_form.html'
    success_url = reverse_lazy('vendas:comissao_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Comissão atualizada com sucesso!')
        return super().form_valid(form)


# Views para Meta de Vendedor
class MetaVendedorListView(LoginRequiredMixin, ListView):
    model = MetaVendedor
    template_name = 'vendas/meta_list.html'
    context_object_name = 'metas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = MetaVendedor.objects.all()
        vendedor = self.request.GET.get('vendedor')
        ano = self.request.GET.get('ano')
        
        if vendedor:
            queryset = queryset.filter(vendedor_id=vendedor)
            
        if ano:
            queryset = queryset.filter(ano=ano)
            
        return queryset.order_by('-ano', '-mes', 'vendedor')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendedores'] = Vendedor.objects.filter(ativo=True)
        context['anos'] = range(2020, datetime.now().year + 2)
        return context


class MetaVendedorCreateView(LoginRequiredMixin, CreateView):
    model = MetaVendedor
    form_class = MetaVendedorForm
    template_name = 'vendas/meta_form.html'
    success_url = reverse_lazy('vendas:meta_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Meta criada com sucesso!')
        return super().form_valid(form)


class MetaVendedorUpdateView(LoginRequiredMixin, UpdateView):
    model = MetaVendedor
    form_class = MetaVendedorForm
    template_name = 'vendas/meta_form.html'
    success_url = reverse_lazy('vendas:meta_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Meta atualizada com sucesso!')
        return super().form_valid(form)


# Views para Relatórios
@login_required
def relatorio_vendas_vendedor(request):
    """Relatório de vendas por vendedor"""
    vendedores = Vendedor.objects.filter(ativo=True)
    ano = request.GET.get('ano', datetime.now().year)
    mes = request.GET.get('mes')
    
    dados = []
    for vendedor in vendedores:
        pedidos = PedidoVenda.objects.filter(
            vendedor=vendedor,
            data_pedido__year=ano
        )
        
        if mes:
            pedidos = pedidos.filter(data_pedido__month=mes)
        
        total_vendas = pedidos.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        quantidade_vendas = pedidos.count()
        
        dados.append({
            'vendedor': vendedor,
            'total_vendas': total_vendas,
            'quantidade_vendas': quantidade_vendas,
        })
    
    context = {
        'dados': dados,
        'ano': ano,
        'mes': mes,
        'anos': range(2020, datetime.now().year + 2),
        'meses': range(1, 13),
    }
    
    return render(request, 'vendas/relatorio_vendas_vendedor.html', context)


@login_required
def relatorio_produtos_mais_vendidos(request):
    """Relatório de produtos mais vendidos"""
    ano = request.GET.get('ano', datetime.now().year)
    mes = request.GET.get('mes')
    
    itens = ItemPedidoVenda.objects.filter(
        pedido__data_pedido__year=ano
    )
    
    if mes:
        itens = itens.filter(pedido__data_pedido__month=mes)
    
    produtos = itens.values(
        'produto__codigo',
        'produto__descricao'
    ).annotate(
        quantidade_vendida=Sum('quantidade'),
        valor_total=Sum('valor_total')
    ).order_by('-quantidade_vendida')[:20]
    
    context = {
        'produtos': produtos,
        'ano': ano,
        'mes': mes,
        'anos': range(2020, datetime.now().year + 2),
        'meses': range(1, 13),
    }
    
    return render(request, 'vendas/relatorio_produtos_mais_vendidos.html', context)


# Views AJAX
@login_required
def converter_orcamento_pedido(request, orcamento_id):
    """Converte orçamento em pedido de venda"""
    if request.method == 'POST':
        orcamento = get_object_or_404(Orcamento, id=orcamento_id)
        
        # Criar pedido baseado no orçamento
        pedido = PedidoVenda.objects.create(
            numero=f"PV{datetime.now().strftime('%Y%m%d%H%M%S')}",
            data_pedido=date.today(),
            data_entrega_prevista=date.today(),
            cliente=orcamento.cliente,
            vendedor=orcamento.vendedor,
            orcamento=orcamento,
            status=StatusPedido.objects.get(codigo='ABERTO'),
            forma_pagamento=orcamento.forma_pagamento,
            valor_produtos=orcamento.valor_produtos,
            valor_desconto=orcamento.valor_desconto,
            percentual_desconto=orcamento.percentual_desconto,
            valor_frete=orcamento.valor_frete,
            valor_total=orcamento.valor_total,
            percentual_comissao=orcamento.vendedor.comissao_percentual,
            observacoes=orcamento.observacoes,
            usuario_criacao=request.user
        )
        
        # Copiar itens do orçamento
        for item_orcamento in orcamento.itens.all():
            ItemPedidoVenda.objects.create(
                pedido=pedido,
                produto=item_orcamento.produto,
                quantidade=item_orcamento.quantidade,
                preco_unitario=item_orcamento.preco_unitario,
                percentual_desconto=item_orcamento.percentual_desconto,
                valor_desconto=item_orcamento.valor_desconto,
                valor_total=item_orcamento.valor_total,
                observacoes=item_orcamento.observacoes
            )
        
        # Atualizar status do orçamento
        orcamento.status = StatusOrcamento.objects.get(codigo='CONVERTIDO')
        orcamento.save()
        
        return JsonResponse({
            'success': True,
            'pedido_id': pedido.id,
            'message': 'Orçamento convertido em pedido com sucesso!'
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


@login_required
def marcar_comissao_paga(request, comissao_id):
    """Marca comissão como paga"""
    if request.method == 'POST':
        comissao = get_object_or_404(ComissaoVendedor, id=comissao_id)
        comissao.pago = True
        comissao.data_pagamento = date.today()
        comissao.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Comissão marcada como paga!'
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

