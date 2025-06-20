from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Cliente, Fornecedor, Produto, Vendedor, Estado, Cidade, TipoPessoa,
    SegmentoMercado, FormaPagamento, UnidadeMedida, CategoriaProduto
)


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'codigo', 'nome_razao_social', 'nome_fantasia', 'tipo_pessoa',
            'cpf_cnpj', 'rg_ie', 'endereco', 'numero', 'complemento', 'bairro',
            'cep', 'cidade', 'telefone', 'celular', 'email', 'site',
            'segmento_mercado', 'forma_pagamento_padrao', 'limite_credito',
            'observacoes'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_pessoa': forms.Select(attrs={'class': 'form-control'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX ou XX.XXX.XXX/XXXX-XX'}),
            'rg_ie': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXXX-XXX'}),
            'cidade': forms.Select(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'site': forms.URLInput(attrs={'class': 'form-control'}),
            'segmento_mercado': forms.Select(attrs={'class': 'form-control'}),
            'forma_pagamento_padrao': forms.Select(attrs={'class': 'form-control'}),
            'limite_credito': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if Cliente.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe um cliente com este código.')
        return codigo


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = [
            'codigo', 'nome_razao_social', 'nome_fantasia', 'tipo_pessoa',
            'cpf_cnpj', 'rg_ie', 'endereco', 'numero', 'complemento', 'bairro',
            'cep', 'cidade', 'telefone', 'celular', 'email', 'site',
            'forma_pagamento_padrao', 'prazo_entrega_dias', 'banco', 'agencia',
            'conta', 'observacoes'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_pessoa': forms.Select(attrs={'class': 'form-control'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX ou XX.XXX.XXX/XXXX-XX'}),
            'rg_ie': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXXX-XXX'}),
            'cidade': forms.Select(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'site': forms.URLInput(attrs={'class': 'form-control'}),
            'forma_pagamento_padrao': forms.Select(attrs={'class': 'form-control'}),
            'prazo_entrega_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'banco': forms.TextInput(attrs={'class': 'form-control'}),
            'agencia': forms.TextInput(attrs={'class': 'form-control'}),
            'conta': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if Fornecedor.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe um fornecedor com este código.')
        return codigo


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'codigo', 'codigo_barras', 'descricao', 'descricao_detalhada',
            'categoria', 'unidade_medida', 'preco_custo', 'preco_venda',
            'margem_lucro', 'estoque_minimo', 'estoque_maximo', 'peso',
            'altura', 'largura', 'profundidade', 'fornecedor_padrao',
            'observacoes'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_detalhada': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'unidade_medida': forms.Select(attrs={'class': 'form-control'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'margem_lucro': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'estoque_maximo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'largura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'profundidade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fornecedor_padrao': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if Produto.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe um produto com este código.')
        return codigo


class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = [
            'codigo', 'nome', 'cpf', 'rg', 'endereco', 'numero', 'complemento',
            'bairro', 'cep', 'cidade', 'telefone', 'celular', 'email',
            'data_admissao', 'data_demissao', 'salario_base', 'comissao_percentual',
            'meta_mensal', 'banco', 'agencia', 'conta', 'observacoes'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXXX-XXX'}),
            'cidade': forms.Select(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'data_admissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_demissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salario_base': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'comissao_percentual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'meta_mensal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'banco': forms.TextInput(attrs={'class': 'form-control'}),
            'agencia': forms.TextInput(attrs={'class': 'form-control'}),
            'conta': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if Vendedor.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe um vendedor com este código.')
        return codigo


# Formulários para Tabelas Auxiliares

class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estado
        fields = ['codigo', 'descricao', 'sigla']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
        }


class CidadeForm(forms.ModelForm):
    class Meta:
        model = Cidade
        fields = ['codigo', 'nome', 'estado', 'codigo_ibge']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'codigo_ibge': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TipoPessoaForm(forms.ModelForm):
    class Meta:
        model = TipoPessoa
        fields = ['codigo', 'descricao']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SegmentoMercadoForm(forms.ModelForm):
    class Meta:
        model = SegmentoMercado
        fields = ['codigo', 'descricao']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FormaPagamentoForm(forms.ModelForm):
    class Meta:
        model = FormaPagamento
        fields = ['codigo', 'descricao', 'prazo_dias']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'prazo_dias': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class UnidadeMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadeMedida
        fields = ['codigo', 'descricao', 'sigla']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '5'}),
        }


class CategoriaProdutoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProduto
        fields = ['codigo', 'descricao', 'categoria_pai']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria_pai': forms.Select(attrs={'class': 'form-control'}),
        }

