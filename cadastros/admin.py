from django.contrib import admin
from .models import (
    Estado, Cidade, TipoPessoa, SegmentoMercado, FormaPagamento,
    UnidadeMedida, CategoriaProduto, Cliente, Fornecedor, Produto, Vendedor
)


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'descricao']
    search_fields = ['sigla', 'descricao']
    ordering = ['sigla']


@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'estado', 'codigo_ibge']
    list_filter = ['estado']
    search_fields = ['nome', 'codigo_ibge']
    ordering = ['estado__sigla', 'nome']


@admin.register(TipoPessoa)
class TipoPessoaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao']
    search_fields = ['codigo', 'descricao']


@admin.register(SegmentoMercado)
class SegmentoMercadoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'ativo']
    list_filter = ['ativo']
    search_fields = ['codigo', 'descricao']


@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'ativo']
    list_filter = ['ativo']
    search_fields = ['codigo', 'descricao']


@admin.register(UnidadeMedida)
class UnidadeMedidaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'ativo']
    list_filter = ['ativo']
    search_fields = ['codigo', 'descricao']


@admin.register(CategoriaProduto)
class CategoriaProdutoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'ativo']
    list_filter = ['ativo']
    search_fields = ['codigo', 'descricao']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome_razao_social', 'cpf_cnpj', 'cidade', 'ativo']
    list_filter = ['ativo', 'tipo_pessoa', 'segmento_mercado', 'cidade__estado']
    search_fields = ['codigo', 'nome_razao_social', 'nome_fantasia', 'cpf_cnpj', 'email']
    ordering = ['codigo']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo', 'nome_razao_social', 'nome_fantasia', 'tipo_pessoa')
        }),
        ('Documentos', {
            'fields': ('cpf_cnpj', 'rg_ie', 'im')
        }),
        ('Endereço', {
            'fields': ('endereco', 'numero', 'complemento', 'bairro', 'cidade', 'cep')
        }),
        ('Contato', {
            'fields': ('telefone', 'celular', 'email', 'site')
        }),
        ('Informações Comerciais', {
            'fields': ('segmento_mercado', 'limite_credito', 'observacoes')
        }),
        ('Status', {
            'fields': ('ativo',)
        })
    )


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome_razao_social', 'cpf_cnpj', 'cidade', 'ativo']
    list_filter = ['ativo', 'tipo_pessoa', 'cidade__estado']
    search_fields = ['codigo', 'nome_razao_social', 'nome_fantasia', 'cpf_cnpj', 'email']
    ordering = ['codigo']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo', 'nome_razao_social', 'nome_fantasia', 'tipo_pessoa')
        }),
        ('Documentos', {
            'fields': ('cpf_cnpj', 'rg_ie', 'im')
        }),
        ('Endereço', {
            'fields': ('endereco', 'numero', 'complemento', 'bairro', 'cidade', 'cep')
        }),
        ('Contato', {
            'fields': ('telefone', 'celular', 'email', 'site')
        }),
        ('Informações Comerciais', {
            'fields': ('observacoes',)
        }),
        ('Status', {
            'fields': ('ativo',)
        })
    )


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'categoria', 'preco_venda', 'estoque_atual', 'ativo']
    list_filter = ['ativo', 'categoria', 'unidade_medida']
    search_fields = ['codigo', 'descricao', 'codigo_barras']
    ordering = ['codigo']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo', 'descricao', 'categoria', 'unidade_medida')
        }),
        ('Códigos', {
            'fields': ('codigo_barras', 'codigo_ncm')
        }),
        ('Preços', {
            'fields': ('custo_compra', 'margem_lucro', 'preco_venda')
        }),
        ('Estoque', {
            'fields': ('estoque_atual', 'estoque_minimo', 'estoque_maximo')
        }),
        ('Dimensões', {
            'fields': ('peso_bruto', 'peso_liquido')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Status', {
            'fields': ('ativo',)
        })
    )


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'email', 'telefone', 'comissao_percentual', 'ativo']
    list_filter = ['ativo']
    search_fields = ['codigo', 'nome', 'email', 'cpf']
    ordering = ['codigo']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('codigo', 'nome', 'cpf', 'rg')
        }),
        ('Contato', {
            'fields': ('telefone', 'celular', 'email')
        }),
        ('Endereço', {
            'fields': ('endereco', 'numero', 'complemento', 'bairro', 'cidade', 'cep')
        }),
        ('Informações Comerciais', {
            'fields': ('comissao_percentual', 'meta_mensal')
        }),
        ('Status', {
            'fields': ('ativo',)
        })
    )

