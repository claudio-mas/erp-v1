from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum, F
from django.http import JsonResponse
from datetime import datetime, date, timedelta
from .models import (
    PlanoContas, CentroCusto, ContasPagar, ContasReceber, FluxoCaixa,
    LancamentoContabil, ItemLancamentoContabil, DRE, TipoConta
)
from .forms import (
    PlanoContasForm, CentroCustoForm, ContasPagarForm, ContasReceberForm,
    FluxoCaixaForm, LancamentoContabilForm, DREForm
)
from cadastros.models import Cliente, Fornecedor


@login_required
def dashboard_financeiro(request):
    """Dashboard do módulo financeiro"""
    hoje = date.today()
    
    # Contas a pagar
    contas_pagar_vencidas = ContasPagar.objects.filter(
        data_vencimento__lt=hoje,
        status='ABERTO'
    )
    contas_pagar_vencer = ContasPagar.objects.filter(
        data_vencimento__gte=hoje,
        data_vencimento__lte=hoje + timedelta(days=30),
        status='ABERTO'
    )
    
    # Contas a receber
    contas_receber_vencidas = ContasReceber.objects.filter(
        data_vencimento__lt=hoje,
        status='ABERTO'
    )
    contas_receber_vencer = ContasReceber.objects.filter(
        data_vencimento__gte=hoje,
        data_vencimento__lte=hoje + timedelta(days=30),
        status='ABERTO'
    )
    
    # Fluxo de caixa do mês
    fluxo_mes = FluxoCaixa.objects.filter(
        data_movimento__month=hoje.month,
        data_movimento__year=hoje.year
    )
    
    entradas_mes = fluxo_mes.filter(tipo_movimento='ENTRADA').aggregate(
        total=Sum('valor')
    )['total'] or 0
    
    saidas_mes = fluxo_mes.filter(tipo_movimento='SAIDA').aggregate(
        total=Sum('valor')
    )['total'] or 0
    
    context = {
        'contas_pagar_vencidas_count': contas_pagar_vencidas.count(),
        'contas_pagar_vencidas_valor': contas_pagar_vencidas.aggregate(Sum('valor_saldo'))['valor_saldo__sum'] or 0,
        'contas_pagar_vencer_count': contas_pagar_vencer.count(),
        'contas_pagar_vencer_valor': contas_pagar_vencer.aggregate(Sum('valor_saldo'))['valor_saldo__sum'] or 0,
        'contas_receber_vencidas_count': contas_receber_vencidas.count(),
        'contas_receber_vencidas_valor': contas_receber_vencidas.aggregate(Sum('valor_saldo'))['valor_saldo__sum'] or 0,
        'contas_receber_vencer_count': contas_receber_vencer.count(),
        'contas_receber_vencer_valor': contas_receber_vencer.aggregate(Sum('valor_saldo'))['valor_saldo__sum'] or 0,
        'entradas_mes': entradas_mes,
        'saidas_mes': saidas_mes,
        'saldo_mes': entradas_mes - saidas_mes,
    }
    return render(request, 'financeiro/dashboard.html', context)


# Views para Plano de Contas
class PlanoContasListView(LoginRequiredMixin, ListView):
    model = PlanoContas
    template_name = 'financeiro/plano_contas_list.html'
    context_object_name = 'contas'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = PlanoContas.objects.filter(ativo=True)
        search = self.request.GET.get('search')
        tipo = self.request.GET.get('tipo')
        
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) |
                Q(descricao__icontains=search)
            )
        
        if tipo:
            queryset = queryset.filter(tipo_conta_id=tipo)
            
        return queryset.order_by('codigo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_conta'] = TipoConta.objects.filter(ativo=True)
        return context


class PlanoContasCreateView(LoginRequiredMixin, CreateView):
    model = PlanoContas
    form_class = PlanoContasForm
    template_name = 'financeiro/plano_contas_form.html'
    success_url = reverse_lazy('financeiro:plano_contas_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Conta criada com sucesso!')
        return super().form_valid(form)


class PlanoContasUpdateView(LoginRequiredMixin, UpdateView):
    model = PlanoContas
    form_class = PlanoContasForm
    template_name = 'financeiro/plano_contas_form.html'
    success_url = reverse_lazy('financeiro:plano_contas_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Conta atualizada com sucesso!')
        return super().form_valid(form)


# Views para Centro de Custo
class CentroCustoListView(LoginRequiredMixin, ListView):
    model = CentroCusto
    template_name = 'financeiro/centro_custo_list.html'
    context_object_name = 'centros'
    paginate_by = 30


class CentroCustoCreateView(LoginRequiredMixin, CreateView):
    model = CentroCusto
    form_class = CentroCustoForm
    template_name = 'financeiro/centro_custo_form.html'
    success_url = reverse_lazy('financeiro:centro_custo_list')


class CentroCustoUpdateView(LoginRequiredMixin, UpdateView):
    model = CentroCusto
    form_class = CentroCustoForm
    template_name = 'financeiro/centro_custo_form.html'
    success_url = reverse_lazy('financeiro:centro_custo_list')


# Views para Contas a Pagar
class ContasPagarListView(LoginRequiredMixin, ListView):
    model = ContasPagar
    template_name = 'financeiro/contas_pagar_list.html'
    context_object_name = 'contas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ContasPagar.objects.all()
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        fornecedor = self.request.GET.get('fornecedor')
        vencimento_inicio = self.request.GET.get('vencimento_inicio')
        vencimento_fim = self.request.GET.get('vencimento_fim')
        
        if search:
            queryset = queryset.filter(
                Q(numero__icontains=search) |
                Q(fornecedor__nome_razao_social__icontains=search) |
                Q(numero_documento__icontains=search)
            )
        
        if status:
            queryset = queryset.filter(status=status)
            
        if fornecedor:
            queryset = queryset.filter(fornecedor_id=fornecedor)
            
        if vencimento_inicio:
            queryset = queryset.filter(data_vencimento__gte=vencimento_inicio)
            
        if vencimento_fim:
            queryset = queryset.filter(data_vencimento__lte=vencimento_fim)
            
        return queryset.order_by('data_vencimento')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = ContasPagar._meta.get_field('status').choices
        context['fornecedores'] = Fornecedor.objects.filter(ativo=True)[:100]
        return context


class ContasPagarDetailView(LoginRequiredMixin, DetailView):
    model = ContasPagar
    template_name = 'financeiro/contas_pagar_detail.html'
    context_object_name = 'conta'


class ContasPagarCreateView(LoginRequiredMixin, CreateView):
    model = ContasPagar
    form_class = ContasPagarForm
    template_name = 'financeiro/contas_pagar_form.html'
    success_url = reverse_lazy('financeiro:contas_pagar_list')
    
    def form_valid(self, form):
        form.instance.usuario_criacao = self.request.user
        messages.success(self.request, 'Conta a pagar criada com sucesso!')
        return super().form_valid(form)


class ContasPagarUpdateView(LoginRequiredMixin, UpdateView):
    model = ContasPagar
    form_class = ContasPagarForm
    template_name = 'financeiro/contas_pagar_form.html'
    success_url = reverse_lazy('financeiro:contas_pagar_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Conta a pagar atualizada com sucesso!')
        return super().form_valid(form)


# Views para Contas a Receber
class ContasReceberListView(LoginRequiredMixin, ListView):
    model = ContasReceber
    template_name = 'financeiro/contas_receber_list.html'
    context_object_name = 'contas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ContasReceber.objects.all()
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        cliente = self.request.GET.get('cliente')
        vencimento_inicio = self.request.GET.get('vencimento_inicio')
        vencimento_fim = self.request.GET.get('vencimento_fim')
        
        if search:
            queryset = queryset.filter(
                Q(numero__icontains=search) |
                Q(cliente__nome_razao_social__icontains=search) |
                Q(numero_documento__icontains=search)
            )
        
        if status:
            queryset = queryset.filter(status=status)
            
        if cliente:
            queryset = queryset.filter(cliente_id=cliente)
            
        if vencimento_inicio:
            queryset = queryset.filter(data_vencimento__gte=vencimento_inicio)
            
        if vencimento_fim:
            queryset = queryset.filter(data_vencimento__lte=vencimento_fim)
            
        return queryset.order_by('data_vencimento')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = ContasReceber._meta.get_field('status').choices
        context['clientes'] = Cliente.objects.filter(ativo=True)[:100]
        return context


class ContasReceberDetailView(LoginRequiredMixin, DetailView):
    model = ContasReceber
    template_name = 'financeiro/contas_receber_detail.html'
    context_object_name = 'conta'


class ContasReceberCreateView(LoginRequiredMixin, CreateView):
    model = ContasReceber
    form_class = ContasReceberForm
    template_name = 'financeiro/contas_receber_form.html'
    success_url = reverse_lazy('financeiro:contas_receber_list')
    
    def form_valid(self, form):
        form.instance.usuario_criacao = self.request.user
        messages.success(self.request, 'Conta a receber criada com sucesso!')
        return super().form_valid(form)


class ContasReceberUpdateView(LoginRequiredMixin, UpdateView):
    model = ContasReceber
    form_class = ContasReceberForm
    template_name = 'financeiro/contas_receber_form.html'
    success_url = reverse_lazy('financeiro:contas_receber_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Conta a receber atualizada com sucesso!')
        return super().form_valid(form)


# Views para Fluxo de Caixa
class FluxoCaixaListView(LoginRequiredMixin, ListView):
    model = FluxoCaixa
    template_name = 'financeiro/fluxo_caixa_list.html'
    context_object_name = 'movimentos'
    paginate_by = 30
    
    def get_queryset(self):
        queryset = FluxoCaixa.objects.all()
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        tipo = self.request.GET.get('tipo')
        
        if data_inicio:
            queryset = queryset.filter(data_movimento__gte=data_inicio)
            
        if data_fim:
            queryset = queryset.filter(data_movimento__lte=data_fim)
            
        if tipo:
            queryset = queryset.filter(tipo_movimento=tipo)
            
        return queryset.order_by('-data_movimento')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_movimento'] = FluxoCaixa._meta.get_field('tipo_movimento').choices
        
        # Calcular totais
        queryset = self.get_queryset()
        context['total_entradas'] = queryset.filter(tipo_movimento='ENTRADA').aggregate(
            total=Sum('valor')
        )['total'] or 0
        context['total_saidas'] = queryset.filter(tipo_movimento='SAIDA').aggregate(
            total=Sum('valor')
        )['total'] or 0
        context['saldo'] = context['total_entradas'] - context['total_saidas']
        
        return context


class FluxoCaixaCreateView(LoginRequiredMixin, CreateView):
    model = FluxoCaixa
    form_class = FluxoCaixaForm
    template_name = 'financeiro/fluxo_caixa_form.html'
    success_url = reverse_lazy('financeiro:fluxo_caixa_list')
    
    def form_valid(self, form):
        form.instance.usuario_criacao = self.request.user
        messages.success(self.request, 'Movimento de caixa criado com sucesso!')
        return super().form_valid(form)


# Views para DRE
class DREListView(LoginRequiredMixin, ListView):
    model = DRE
    template_name = 'financeiro/dre_list.html'
    context_object_name = 'dres'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = DRE.objects.all()
        ano = self.request.GET.get('ano')
        
        if ano:
            queryset = queryset.filter(ano=ano)
            
        return queryset.order_by('-ano', '-mes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anos'] = range(2020, datetime.now().year + 2)
        return context


class DREDetailView(LoginRequiredMixin, DetailView):
    model = DRE
    template_name = 'financeiro/dre_detail.html'
    context_object_name = 'dre'


class DRECreateView(LoginRequiredMixin, CreateView):
    model = DRE
    form_class = DREForm
    template_name = 'financeiro/dre_form.html'
    success_url = reverse_lazy('financeiro:dre_list')
    
    def form_valid(self, form):
        form.instance.usuario_criacao = self.request.user
        messages.success(self.request, 'DRE criada com sucesso!')
        return super().form_valid(form)


class DREUpdateView(LoginRequiredMixin, UpdateView):
    model = DRE
    form_class = DREForm
    template_name = 'financeiro/dre_form.html'
    success_url = reverse_lazy('financeiro:dre_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'DRE atualizada com sucesso!')
        return super().form_valid(form)


# Views para Relatórios
@login_required
def relatorio_contas_pagar_vencer(request):
    """Relatório de contas a pagar a vencer"""
    dias = int(request.GET.get('dias', 30))
    hoje = date.today()
    data_limite = hoje + timedelta(days=dias)
    
    contas = ContasPagar.objects.filter(
        data_vencimento__gte=hoje,
        data_vencimento__lte=data_limite,
        status='ABERTO'
    ).order_by('data_vencimento')
    
    total_valor = contas.aggregate(Sum('valor_saldo'))['valor_saldo__sum'] or 0
    
    context = {
        'contas': contas,
        'total_valor': total_valor,
        'dias': dias,
        'data_limite': data_limite,
    }
    
    return render(request, 'financeiro/relatorio_contas_pagar_vencer.html', context)


@login_required
def relatorio_contas_receber_vencer(request):
    """Relatório de contas a receber a vencer"""
    dias = int(request.GET.get('dias', 30))
    hoje = date.today()
    data_limite = hoje + timedelta(days=dias)
    
    contas = ContasReceber.objects.filter(
        data_vencimento__gte=hoje,
        data_vencimento__lte=data_limite,
        status='ABERTO'
    ).order_by('data_vencimento')
    
    total_valor = contas.aggregate(Sum('valor_saldo'))['valor_saldo__sum'] or 0
    
    context = {
        'contas': contas,
        'total_valor': total_valor,
        'dias': dias,
        'data_limite': data_limite,
    }
    
    return render(request, 'financeiro/relatorio_contas_receber_vencer.html', context)


@login_required
def relatorio_fluxo_caixa_periodo(request):
    """Relatório de fluxo de caixa por período"""
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    if not data_inicio:
        data_inicio = date.today().replace(day=1)
    if not data_fim:
        data_fim = date.today()
    
    movimentos = FluxoCaixa.objects.filter(
        data_movimento__gte=data_inicio,
        data_movimento__lte=data_fim
    ).order_by('data_movimento')
    
    # Agrupar por data
    movimentos_por_data = {}
    for movimento in movimentos:
        data = movimento.data_movimento
        if data not in movimentos_por_data:
            movimentos_por_data[data] = {'entradas': 0, 'saidas': 0}
        
        if movimento.tipo_movimento == 'ENTRADA':
            movimentos_por_data[data]['entradas'] += movimento.valor
        else:
            movimentos_por_data[data]['saidas'] += movimento.valor
    
    # Calcular saldo acumulado
    saldo_acumulado = 0
    dados_grafico = []
    for data in sorted(movimentos_por_data.keys()):
        entradas = movimentos_por_data[data]['entradas']
        saidas = movimentos_por_data[data]['saidas']
        saldo_dia = entradas - saidas
        saldo_acumulado += saldo_dia
        
        dados_grafico.append({
            'data': data,
            'entradas': entradas,
            'saidas': saidas,
            'saldo_dia': saldo_dia,
            'saldo_acumulado': saldo_acumulado
        })
    
    total_entradas = sum(d['entradas'] for d in dados_grafico)
    total_saidas = sum(d['saidas'] for d in dados_grafico)
    
    context = {
        'dados_grafico': dados_grafico,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo_periodo': total_entradas - total_saidas,
    }
    
    return render(request, 'financeiro/relatorio_fluxo_caixa_periodo.html', context)


# Views AJAX
@login_required
def pagar_conta(request, conta_id):
    """Marca conta como paga"""
    if request.method == 'POST':
        conta = get_object_or_404(ContasPagar, id=conta_id)
        valor_pago = float(request.POST.get('valor_pago', conta.valor_saldo))
        
        conta.valor_pago += valor_pago
        conta.data_pagamento = date.today()
        conta.save()  # O save() já atualiza o status automaticamente
        
        # Criar movimento no fluxo de caixa
        FluxoCaixa.objects.create(
            data_movimento=date.today(),
            conta_contabil=conta.conta_contabil,
            centro_custo=conta.centro_custo,
            tipo_movimento='SAIDA',
            valor=valor_pago,
            conta_pagar=conta,
            descricao=f"Pagamento - {conta.fornecedor.nome_razao_social}",
            numero_documento=conta.numero_documento,
            usuario_criacao=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Conta paga com sucesso!',
            'novo_status': conta.status
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


@login_required
def receber_conta(request, conta_id):
    """Marca conta como recebida"""
    if request.method == 'POST':
        conta = get_object_or_404(ContasReceber, id=conta_id)
        valor_recebido = float(request.POST.get('valor_recebido', conta.valor_saldo))
        
        conta.valor_recebido += valor_recebido
        conta.data_recebimento = date.today()
        conta.save()  # O save() já atualiza o status automaticamente
        
        # Criar movimento no fluxo de caixa
        FluxoCaixa.objects.create(
            data_movimento=date.today(),
            conta_contabil=conta.conta_contabil,
            centro_custo=conta.centro_custo,
            tipo_movimento='ENTRADA',
            valor=valor_recebido,
            conta_receber=conta,
            descricao=f"Recebimento - {conta.cliente.nome_razao_social}",
            numero_documento=conta.numero_documento,
            usuario_criacao=request.user
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Conta recebida com sucesso!',
            'novo_status': conta.status
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})

