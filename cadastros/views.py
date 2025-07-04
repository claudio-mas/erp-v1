from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .models import (
    Cliente, Fornecedor, Produto, Vendedor, Estado, Cidade, TipoPessoa,
    SegmentoMercado, FormaPagamento, UnidadeMedida, CategoriaProduto
)
from .forms import (
    ClienteForm, FornecedorForm, ProdutoForm, VendedorForm, EstadoForm,
    CidadeForm, TipoPessoaForm, SegmentoMercadoForm, FormaPagamentoForm,
    UnidadeMedidaForm, CategoriaProdutoForm
)


@login_required
def dashboard_cadastros(request):
    """Dashboard do módulo de cadastros"""
    context = {
        'total_clientes': Cliente.objects.filter(ativo=True).count(),
        'total_fornecedores': Fornecedor.objects.filter(ativo=True).count(),
        'total_produtos': Produto.objects.filter(ativo=True).count(),
        'total_vendedores': Vendedor.objects.filter(ativo=True).count(),
    }
    return render(request, 'cadastros/dashboard.html', context)


# Views para Cliente
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'cadastros/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Cliente.objects.select_related('cidade__estado', 'tipo_pessoa')
        
        # Filtro de status ativo/inativo
        ativo = self.request.GET.get('ativo')
        if ativo == 'true':
            queryset = queryset.filter(ativo=True)
        elif ativo == 'false':
            queryset = queryset.filter(ativo=False)
        else:
            queryset = queryset.filter(ativo=True)  # Padrão: apenas ativos
        
        # Filtro de busca
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nome_razao_social__icontains=search) |
                Q(cpf_cnpj__icontains=search) |
                Q(codigo__icontains=search)
            )
        
        # Filtro por tipo de pessoa
        tipo_pessoa = self.request.GET.get('tipo_pessoa')
        if tipo_pessoa:
            queryset = queryset.filter(tipo_pessoa_id=tipo_pessoa)
        
        return queryset.order_by('nome_razao_social')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_pessoa'] = TipoPessoa.objects.filter(ativo=True)
        return context

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'cadastros/cliente_detail.html'
    context_object_name = 'cliente'


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cadastros/cliente_form.html'
    success_url = reverse_lazy('cadastros:cliente_list')
    
    def form_valid(self, form):
        form.instance.usuario_cadastro = self.request.user
        messages.success(self.request, 'Cliente cadastrado com sucesso!')
        return super().form_valid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cadastros/cliente_form.html'
    success_url = reverse_lazy('cadastros:cliente_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return super().form_valid(form)


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'cadastros/cliente_confirm_delete.html'
    success_url = reverse_lazy('cadastros:cliente_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.ativo = False
        self.object.save()
        messages.success(request, 'Cliente inativado com sucesso!')
        return redirect(self.success_url)


# Views para Fornecedor
class FornecedorListView(LoginRequiredMixin, ListView):
    model = Fornecedor
    template_name = 'cadastros/fornecedor_list.html'
    context_object_name = 'fornecedores'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Fornecedor.objects.filter(ativo=True)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nome_razao_social__icontains=search) |
                Q(cpf_cnpj__icontains=search) |
                Q(codigo__icontains=search)
            )
        return queryset.order_by('nome_razao_social')


class FornecedorDetailView(LoginRequiredMixin, DetailView):
    model = Fornecedor
    template_name = 'cadastros/fornecedor_detail.html'
    context_object_name = 'fornecedor'


class FornecedorCreateView(LoginRequiredMixin, CreateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'cadastros/fornecedor_form.html'
    success_url = reverse_lazy('cadastros:fornecedor_list')
    
    def form_valid(self, form):
        form.instance.usuario_cadastro = self.request.user
        messages.success(self.request, 'Fornecedor cadastrado com sucesso!')
        return super().form_valid(form)


class FornecedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'cadastros/fornecedor_form.html'
    success_url = reverse_lazy('cadastros:fornecedor_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Fornecedor atualizado com sucesso!')
        return super().form_valid(form)


class FornecedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Fornecedor
    template_name = 'cadastros/fornecedor_confirm_delete.html'
    success_url = reverse_lazy('cadastros:fornecedor_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.ativo = False
        self.object.save()
        messages.success(request, 'Fornecedor inativado com sucesso!')
        return redirect(self.success_url)


# Views para Produto
class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'cadastros/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Produto.objects.filter(ativo=True)
        search = self.request.GET.get('search')
        categoria = self.request.GET.get('categoria')
        
        if search:
            queryset = queryset.filter(
                Q(descricao__icontains=search) |
                Q(codigo__icontains=search) |
                Q(codigo_barras__icontains=search)
            )
        
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
            
        return queryset.order_by('descricao')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = CategoriaProduto.objects.filter(ativo=True)
        return context


class ProdutoDetailView(LoginRequiredMixin, DetailView):
    model = Produto
    template_name = 'cadastros/produto_detail.html'
    context_object_name = 'produto'


class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'cadastros/produto_form.html'
    success_url = reverse_lazy('cadastros:produto_list')
    
    def form_valid(self, form):
        form.instance.usuario_cadastro = self.request.user
        messages.success(self.request, 'Produto cadastrado com sucesso!')
        return super().form_valid(form)


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'cadastros/produto_form.html'
    success_url = reverse_lazy('cadastros:produto_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Produto atualizado com sucesso!')
        return super().form_valid(form)


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = 'cadastros/produto_confirm_delete.html'
    success_url = reverse_lazy('cadastros:produto_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.ativo = False
        self.object.save()
        messages.success(request, 'Produto inativado com sucesso!')
        return redirect(self.success_url)


# Views para Vendedor
class VendedorListView(LoginRequiredMixin, ListView):
    model = Vendedor
    template_name = 'cadastros/vendedor_list.html'
    context_object_name = 'vendedores'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Vendedor.objects.filter(ativo=True)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(cpf__icontains=search) |
                Q(codigo__icontains=search)
            )
        return queryset.order_by('nome')


class VendedorDetailView(LoginRequiredMixin, DetailView):
    model = Vendedor
    template_name = 'cadastros/vendedor_detail.html'
    context_object_name = 'vendedor'


class VendedorCreateView(LoginRequiredMixin, CreateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'cadastros/vendedor_form.html'
    success_url = reverse_lazy('cadastros:vendedor_list')
    
    def form_valid(self, form):
        form.instance.usuario_cadastro = self.request.user
        messages.success(self.request, 'Vendedor cadastrado com sucesso!')
        return super().form_valid(form)


class VendedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'cadastros/vendedor_form.html'
    success_url = reverse_lazy('cadastros:vendedor_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Vendedor atualizado com sucesso!')
        return super().form_valid(form)


class VendedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Vendedor
    template_name = 'cadastros/vendedor_confirm_delete.html'
    success_url = reverse_lazy('cadastros:vendedor_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.ativo = False
        self.object.save()
        messages.success(request, 'Vendedor inativado com sucesso!')
        return redirect(self.success_url)


# Views para Tabelas Auxiliares

# Estado
class EstadoListView(LoginRequiredMixin, ListView):
    model = Estado
    template_name = 'cadastros/estado_list.html'
    context_object_name = 'estados'
    paginate_by = 30


class EstadoCreateView(LoginRequiredMixin, CreateView):
    model = Estado
    form_class = EstadoForm
    template_name = 'cadastros/estado_form.html'
    success_url = reverse_lazy('cadastros:estado_list')


class EstadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Estado
    form_class = EstadoForm
    template_name = 'cadastros/estado_form.html'
    success_url = reverse_lazy('cadastros:estado_list')


# Cidade
class CidadeListView(LoginRequiredMixin, ListView):
    model = Cidade
    template_name = 'cadastros/cidade_list.html'
    context_object_name = 'cidades'
    paginate_by = 30
    
    def get_queryset(self):
        queryset = Cidade.objects.filter(ativo=True)
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado_id=estado)
        return queryset.order_by('nome')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = Estado.objects.filter(ativo=True)
        return context


class CidadeCreateView(LoginRequiredMixin, CreateView):
    model = Cidade
    form_class = CidadeForm
    template_name = 'cadastros/cidade_form.html'
    success_url = reverse_lazy('cadastros:cidade_list')


class CidadeUpdateView(LoginRequiredMixin, UpdateView):
    model = Cidade
    form_class = CidadeForm
    template_name = 'cadastros/cidade_form.html'
    success_url = reverse_lazy('cadastros:cidade_list')


# Views AJAX para busca dinâmica
@login_required
def buscar_cidades_por_estado(request):
    """Busca cidades por estado via AJAX"""
    estado_id = request.GET.get('estado_id')
    cidades = Cidade.objects.filter(estado_id=estado_id, ativo=True).values('id', 'nome')
    return JsonResponse(list(cidades), safe=False)


@login_required
def buscar_produtos(request):
    """Busca produtos via AJAX"""
    term = request.GET.get('term', '')
    produtos = Produto.objects.filter(
        Q(descricao__icontains=term) | Q(codigo__icontains=term),
        ativo=True
    )[:10]
    
    results = []
    for produto in produtos:
        results.append({
            'id': produto.id,
            'label': f"{produto.codigo} - {produto.descricao}",
            'value': produto.descricao,
            'preco': str(produto.preco_venda)
        })
    
    return JsonResponse(results, safe=False)


@login_required
def buscar_clientes(request):
    """Busca clientes via AJAX"""
    term = request.GET.get('term', '')
    clientes = Cliente.objects.filter(
        Q(nome_razao_social__icontains=term) | Q(codigo__icontains=term),
        ativo=True
    )[:10]
    
    results = []
    for cliente in clientes:
        results.append({
            'id': cliente.id,
            'label': f"{cliente.codigo} - {cliente.nome_razao_social}",
            'value': cliente.nome_razao_social
        })
    
    return JsonResponse(results, safe=False)


@login_required
def buscar_fornecedores(request):
    """Busca fornecedores via AJAX"""
    term = request.GET.get('term', '')
    fornecedores = Fornecedor.objects.filter(
        Q(nome_razao_social__icontains=term) | Q(codigo__icontains=term),
        ativo=True
    )[:10]
    
    results = []
    for fornecedor in fornecedores:
        results.append({
            'id': fornecedor.id,
            'label': f"{fornecedor.codigo} - {fornecedor.nome_razao_social}",
            'value': fornecedor.nome_razao_social
        })
    
    return JsonResponse(results, safe=False)


@login_required
def exportar_clientes_csv(request):
    """Exporta lista de clientes para CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'
    response.write('\ufeff')  # BOM para UTF-8
    
    writer = csv.writer(response)
    writer.writerow([
        'Código', 'Nome/Razão Social', 'Nome Fantasia', 'CPF/CNPJ', 
        'Telefone', 'Celular', 'Email', 'Cidade', 'Estado', 'Status'
    ])
    
    # Aplicar os mesmos filtros da listagem
    queryset = Cliente.objects.select_related('cidade__estado')
    
    ativo = request.GET.get('ativo')
    if ativo == 'true':
        queryset = queryset.filter(ativo=True)
    elif ativo == 'false':
        queryset = queryset.filter(ativo=False)
    else:
        queryset = queryset.filter(ativo=True)
    
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(nome_razao_social__icontains=search) |
            Q(cpf_cnpj__icontains=search) |
            Q(codigo__icontains=search)
        )
    
    tipo_pessoa = request.GET.get('tipo_pessoa')
    if tipo_pessoa:
        queryset = queryset.filter(tipo_pessoa_id=tipo_pessoa)
    
    for cliente in queryset.order_by('nome_razao_social'):
        writer.writerow([
            cliente.codigo,
            cliente.nome_razao_social,
            cliente.nome_fantasia or '',
            cliente.cpf_cnpj,
            cliente.telefone or '',
            cliente.celular or '',
            cliente.email or '',
            cliente.cidade.nome,
            cliente.cidade.estado.sigla,
            'Ativo' if cliente.ativo else 'Inativo'
        ])
    
    return response


@login_required
def imprimir_clientes_pdf(request):
    """Gera PDF para impressão da lista de clientes"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="clientes.pdf"'
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    # Aplicar os mesmos filtros da listagem
    queryset = Cliente.objects.select_related('cidade__estado')
    
    ativo = request.GET.get('ativo')
    if ativo == 'true':
        queryset = queryset.filter(ativo=True)
    elif ativo == 'false':
        queryset = queryset.filter(ativo=False)
    else:
        queryset = queryset.filter(ativo=True)
    
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(nome_razao_social__icontains=search) |
            Q(cpf_cnpj__icontains=search) |
            Q(codigo__icontains=search)
        )
    
    tipo_pessoa = request.GET.get('tipo_pessoa')
    if tipo_pessoa:
        queryset = queryset.filter(tipo_pessoa_id=tipo_pessoa)
    
    # Preparar dados para a tabela
    data = [['Código', 'Nome/Razão Social', 'CPF/CNPJ', 'Cidade', 'Status']]
    
    for cliente in queryset.order_by('nome_razao_social'):
        data.append([
            cliente.codigo,
            cliente.nome_razao_social[:30] + '...' if len(cliente.nome_razao_social) > 30 else cliente.nome_razao_social,
            cliente.cpf_cnpj,
            f"{cliente.cidade.nome}-{cliente.cidade.estado.sigla}",
            'Ativo' if cliente.ativo else 'Inativo'
        ])
    
    # Criar tabela
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    # Título
    styles = getSampleStyleSheet()
    title = Paragraph("Lista de Clientes", styles['Title'])
    
    # Construir documento
    elements = [title, table]
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response

