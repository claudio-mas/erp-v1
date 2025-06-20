from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum, F
from django.db import models
from django.http import JsonResponse
from datetime import datetime, date
from .models import (
    MovimentacaoEstoque, EstoqueProduto, Inventario, ItemInventario,
    ReservaProduto, ProdutoFornecedor, TipoMovimentacao, LocalEstoque
)
from .forms import (
    MovimentacaoEstoqueForm, InventarioForm, ItemInventarioForm,
    ReservaProdutoForm, ProdutoFornecedorForm
)
from cadastros.models import Produto, Fornecedor
from vendas.models import PedidoVenda


@login_required
def dashboard_estoque(request):
    """Dashboard do módulo de estoque"""
    context = {
        'produtos_estoque_baixo': Produto.objects.filter(
            estoque_atual__lt=F('estoque_minimo'),
            ativo=True
        ).count(),
        'total_produtos_estoque': Produto.objects.filter(ativo=True).count(),
        'movimentacoes_hoje': MovimentacaoEstoque.objects.filter(
            data_movimentacao__date=date.today()
        ).count(),
        'inventarios_abertos': Inventario.objects.filter(
            status='EM_ANDAMENTO'
        ).count(),
        'reservas_ativas': ReservaProduto.objects.filter(ativa=True).count(),
    }
    return render(request, 'estoque/dashboard.html', context)


# Views para Movimentação de Estoque
class MovimentacaoEstoqueListView(LoginRequiredMixin, ListView):
    model = MovimentacaoEstoque
    template_name = 'estoque/movimentacao_list.html'
    context_object_name = 'movimentacoes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = MovimentacaoEstoque.objects.all()
        search = self.request.GET.get('search')
        tipo = self.request.GET.get('tipo')
        produto = self.request.GET.get('produto')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        
        if search:
            queryset = queryset.filter(
                Q(numero__icontains=search) |
                Q(produto__descricao__icontains=search) |
                Q(produto__codigo__icontains=search)
            )
        
        if tipo:
            queryset = queryset.filter(tipo_movimentacao__tipo=tipo)
            
        if produto:
            queryset = queryset.filter(produto_id=produto)
            
        if data_inicio:
            queryset = queryset.filter(data_movimentacao__date__gte=data_inicio)
            
        if data_fim:
            queryset = queryset.filter(data_movimentacao__date__lte=data_fim)
            
        return queryset.order_by('-data_movimentacao')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_movimentacao'] = TipoMovimentacao.objects.filter(ativo=True)
        context['produtos'] = Produto.objects.filter(ativo=True)[:100]  # Limitar para performance
        return context


class MovimentacaoEstoqueDetailView(LoginRequiredMixin, DetailView):
    model = MovimentacaoEstoque
    template_name = 'estoque/movimentacao_detail.html'
    context_object_name = 'movimentacao'


class MovimentacaoEstoqueCreateView(LoginRequiredMixin, CreateView):
    model = MovimentacaoEstoque
    form_class = MovimentacaoEstoqueForm
    template_name = 'estoque/movimentacao_form.html'
    success_url = reverse_lazy('estoque:movimentacao_list')
    
    def form_valid(self, form):
        form.instance.usuario_criacao = self.request.user
        messages.success(self.request, 'Movimentação de estoque criada com sucesso!')
        return super().form_valid(form)


# Views para Estoque de Produtos
class EstoqueProdutoListView(LoginRequiredMixin, ListView):
    model = EstoqueProduto
    template_name = 'estoque/estoque_produto_list.html'
    context_object_name = 'estoques'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = EstoqueProduto.objects.all()
        search = self.request.GET.get('search')
        local = self.request.GET.get('local')
        estoque_baixo = self.request.GET.get('estoque_baixo')
        
        if search:
            queryset = queryset.filter(
                Q(produto__descricao__icontains=search) |
                Q(produto__codigo__icontains=search)
            )
        
        if local:
            queryset = queryset.filter(local_estoque_id=local)
            
        if estoque_baixo:
            queryset = queryset.filter(
                quantidade_atual__lt=F('produto__estoque_minimo')
            )
            
        return queryset.order_by('produto__descricao')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locais_estoque'] = LocalEstoque.objects.filter(ativo=True)
        return context


class EstoqueProdutoDetailView(LoginRequiredMixin, DetailView):
    model = EstoqueProduto
    template_name = 'estoque/estoque_produto_detail.html'
    context_object_name = 'estoque'


# Views para Inventário
class InventarioListView(LoginRequiredMixin, ListView):
    model = Inventario
    template_name = 'estoque/inventario_list.html'
    context_object_name = 'inventarios'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Inventario.objects.all()
        status = self.request.GET.get('status')
        local = self.request.GET.get('local')
        
        if status:
            queryset = queryset.filter(status=status)
            
        if local:
            queryset = queryset.filter(local_estoque_id=local)
            
        return queryset.order_by('-data_inventario')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Inventario._meta.get_field('status').choices
        context['locais_estoque'] = LocalEstoque.objects.filter(ativo=True)
        return context


class InventarioDetailView(LoginRequiredMixin, DetailView):
    model = Inventario
    template_name = 'estoque/inventario_detail.html'
    context_object_name = 'inventario'


class InventarioCreateView(LoginRequiredMixin, CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'estoque/inventario_form.html'
    success_url = reverse_lazy('estoque:inventario_list')
    
    def form_valid(self, form):
        form.instance.usuario_criacao = self.request.user
        messages.success(self.request, 'Inventário criado com sucesso!')
        return super().form_valid(form)


class InventarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'estoque/inventario_form.html'
    success_url = reverse_lazy('estoque:inventario_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Inventário atualizado com sucesso!')
        return super().form_valid(form)


# Views para Reserva de Produto
class ReservaProdutoListView(LoginRequiredMixin, ListView):
    model = ReservaProduto
    template_name = 'estoque/reserva_list.html'
    context_object_name = 'reservas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ReservaProduto.objects.filter(ativa=True)
        search = self.request.GET.get('search')
        produto = self.request.GET.get('produto')
        
        if search:
            queryset = queryset.filter(
                Q(produto__descricao__icontains=search) |
                Q(produto__codigo__icontains=search) |
                Q(pedido_venda__numero__icontains=search)
            )
        
        if produto:
            queryset = queryset.filter(produto_id=produto)
            
        return queryset.order_by('-data_reserva')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.filter(ativo=True)[:100]
        return context


class ReservaProdutoDetailView(LoginRequiredMixin, DetailView):
    model = ReservaProduto
    template_name = 'estoque/reserva_detail.html'
    context_object_name = 'reserva'


class ReservaProdutoCreateView(LoginRequiredMixin, CreateView):
    model = ReservaProduto
    form_class = ReservaProdutoForm
    template_name = 'estoque/reserva_form.html'
    success_url = reverse_lazy('estoque:reserva_list')
    
    def form_valid(self, form):
        form.instance.usuario_reserva = self.request.user
        messages.success(self.request, 'Reserva criada com sucesso!')
        return super().form_valid(form)


# Views para Produto x Fornecedor
class ProdutoFornecedorListView(LoginRequiredMixin, ListView):
    model = ProdutoFornecedor
    template_name = 'estoque/produto_fornecedor_list.html'
    context_object_name = 'produto_fornecedores'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ProdutoFornecedor.objects.filter(ativo=True)
        search = self.request.GET.get('search')
        produto = self.request.GET.get('produto')
        fornecedor = self.request.GET.get('fornecedor')
        
        if search:
            queryset = queryset.filter(
                Q(produto__descricao__icontains=search) |
                Q(produto__codigo__icontains=search) |
                Q(fornecedor__nome_razao_social__icontains=search)
            )
        
        if produto:
            queryset = queryset.filter(produto_id=produto)
            
        if fornecedor:
            queryset = queryset.filter(fornecedor_id=fornecedor)
            
        return queryset.order_by('produto__descricao', 'fornecedor__nome_razao_social')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.filter(ativo=True)[:100]
        context['fornecedores'] = Fornecedor.objects.filter(ativo=True)[:100]
        return context


class ProdutoFornecedorCreateView(LoginRequiredMixin, CreateView):
    model = ProdutoFornecedor
    form_class = ProdutoFornecedorForm
    template_name = 'estoque/produto_fornecedor_form.html'
    success_url = reverse_lazy('estoque:produto_fornecedor_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Relacionamento produto-fornecedor criado com sucesso!')
        return super().form_valid(form)


class ProdutoFornecedorUpdateView(LoginRequiredMixin, UpdateView):
    model = ProdutoFornecedor
    form_class = ProdutoFornecedorForm
    template_name = 'estoque/produto_fornecedor_form.html'
    success_url = reverse_lazy('estoque:produto_fornecedor_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Relacionamento produto-fornecedor atualizado com sucesso!')
        return super().form_valid(form)


# Views para Relatórios
@login_required
def relatorio_estoque_baixo(request):
    """Relatório de produtos com estoque baixo"""
    produtos = Produto.objects.filter(
        estoque_atual__lt=F('estoque_minimo'),
        ativo=True
    ).order_by('descricao')
    
    context = {
        'produtos': produtos,
        'total_produtos': produtos.count(),
    }
    
    return render(request, 'estoque/relatorio_estoque_baixo.html', context)


@login_required
def relatorio_movimentacoes_periodo(request):
    """Relatório de movimentações por período"""
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    tipo = request.GET.get('tipo')
    
    movimentacoes = MovimentacaoEstoque.objects.all()
    
    if data_inicio:
        movimentacoes = movimentacoes.filter(data_movimentacao__date__gte=data_inicio)
    
    if data_fim:
        movimentacoes = movimentacoes.filter(data_movimentacao__date__lte=data_fim)
    
    if tipo:
        movimentacoes = movimentacoes.filter(tipo_movimentacao__tipo=tipo)
    
    # Agrupar por produto
    produtos_movimentados = movimentacoes.values(
        'produto__codigo',
        'produto__descricao'
    ).annotate(
        total_entradas=Sum('quantidade', filter=Q(tipo_movimentacao__tipo='E')),
        total_saidas=Sum('quantidade', filter=Q(tipo_movimentacao__tipo='S')),
        valor_total=Sum('custo_total')
    ).order_by('produto__descricao')
    
    context = {
        'produtos_movimentados': produtos_movimentados,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'tipo': tipo,
        'tipos_movimentacao': [('E', 'Entrada'), ('S', 'Saída')],
    }
    
    return render(request, 'estoque/relatorio_movimentacoes_periodo.html', context)


@login_required
def relatorio_inventario(request, inventario_id):
    """Relatório de inventário"""
    inventario = get_object_or_404(Inventario, id=inventario_id)
    itens = inventario.itens.all().order_by('produto__descricao')
    
    # Calcular totais
    total_diferenca_valor = sum(item.valor_diferenca for item in itens)
    itens_com_diferenca = itens.filter(diferenca__ne=0).count()
    
    context = {
        'inventario': inventario,
        'itens': itens,
        'total_diferenca_valor': total_diferenca_valor,
        'itens_com_diferenca': itens_com_diferenca,
        'total_itens': itens.count(),
    }
    
    return render(request, 'estoque/relatorio_inventario.html', context)


# Views AJAX
@login_required
def liberar_reserva(request, reserva_id):
    """Libera reserva de produto"""
    if request.method == 'POST':
        reserva = get_object_or_404(ReservaProduto, id=reserva_id)
        reserva.ativa = False
        reserva.data_liberacao = datetime.now()
        reserva.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Reserva liberada com sucesso!'
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


@login_required
def ajustar_estoque_inventario(request, item_id):
    """Ajusta estoque baseado no inventário"""
    if request.method == 'POST':
        item = get_object_or_404(ItemInventario, id=item_id)
        
        if item.diferenca != 0:
            # Criar movimentação de ajuste
            tipo_mov = TipoMovimentacao.objects.get(
                codigo='AJUSTE_INV'
            )
            
            MovimentacaoEstoque.objects.create(
                numero=f"AJ{datetime.now().strftime('%Y%m%d%H%M%S')}",
                data_movimentacao=datetime.now(),
                produto=item.produto,
                local_estoque=item.inventario.local_estoque,
                tipo_movimentacao=tipo_mov,
                quantidade=abs(item.diferenca),
                quantidade_anterior=item.quantidade_sistema,
                quantidade_atual=item.quantidade_contada,
                custo_unitario=item.custo_unitario,
                documento_referencia=f"Inventário {item.inventario.numero}",
                observacoes=f"Ajuste de inventário - Diferença: {item.diferenca}",
                usuario_criacao=request.user
            )
            
            # Marcar item como ajustado
            item.ajustado = True
            item.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Estoque ajustado com sucesso!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Não há diferença para ajustar!'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


@login_required
def buscar_estoque_produto(request):
    """Busca estoque atual de um produto"""
    produto_id = request.GET.get('produto_id')
    local_id = request.GET.get('local_id')
    
    try:
        estoque = EstoqueProduto.objects.get(
            produto_id=produto_id,
            local_estoque_id=local_id
        )
        return JsonResponse({
            'success': True,
            'quantidade_atual': str(estoque.quantidade_atual),
            'quantidade_disponivel': str(estoque.quantidade_disponivel),
            'custo_medio': str(estoque.custo_medio)
        })
    except EstoqueProduto.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Estoque não encontrado'
        })

