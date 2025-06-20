from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Orcamento, ItemOrcamento, PedidoVenda, ItemPedidoVenda,
    ComissaoVendedor, MetaVendedor, StatusOrcamento, StatusPedido
)
from cadastros.models import Cliente, Produto, Vendedor, FormaPagamento


class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = [
            'numero', 'data_orcamento', 'data_validade', 'cliente', 'vendedor',
            'status', 'forma_pagamento', 'valor_produtos', 'valor_desconto',
            'percentual_desconto', 'valor_frete', 'observacoes', 'observacoes_internas'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'data_orcamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_validade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'vendedor': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'valor_produtos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
            'valor_desconto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'percentual_desconto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_frete': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observacoes_internas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if Orcamento.objects.filter(numero=numero).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe um orçamento com este número.')
        return numero

    def clean(self):
        cleaned_data = super().clean()
        data_orcamento = cleaned_data.get('data_orcamento')
        data_validade = cleaned_data.get('data_validade')
        
        if data_orcamento and data_validade:
            if data_validade < data_orcamento:
                raise ValidationError('A data de validade deve ser posterior à data do orçamento.')
        
        return cleaned_data


class ItemOrcamentoForm(forms.ModelForm):
    class Meta:
        model = ItemOrcamento
        fields = [
            'produto', 'quantidade', 'preco_unitario', 'percentual_desconto',
            'observacoes'
        ]
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'percentual_desconto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        if quantidade <= 0:
            raise ValidationError('A quantidade deve ser maior que zero.')
        return quantidade

    def clean_preco_unitario(self):
        preco_unitario = self.cleaned_data['preco_unitario']
        if preco_unitario <= 0:
            raise ValidationError('O preço unitário deve ser maior que zero.')
        return preco_unitario


class PedidoVendaForm(forms.ModelForm):
    class Meta:
        model = PedidoVenda
        fields = [
            'numero', 'data_pedido', 'data_entrega_prevista', 'cliente', 'vendedor',
            'orcamento', 'status', 'forma_pagamento', 'valor_produtos', 'valor_desconto',
            'percentual_desconto', 'valor_frete', 'percentual_comissao',
            'observacoes', 'observacoes_internas'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'data_pedido': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_entrega_prevista': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'vendedor': forms.Select(attrs={'class': 'form-control'}),
            'orcamento': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'valor_produtos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
            'valor_desconto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'percentual_desconto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_frete': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'percentual_comissao': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observacoes_internas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if PedidoVenda.objects.filter(numero=numero).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe um pedido com este número.')
        return numero

    def clean(self):
        cleaned_data = super().clean()
        data_pedido = cleaned_data.get('data_pedido')
        data_entrega_prevista = cleaned_data.get('data_entrega_prevista')
        
        if data_pedido and data_entrega_prevista:
            if data_entrega_prevista < data_pedido:
                raise ValidationError('A data de entrega prevista deve ser posterior à data do pedido.')
        
        return cleaned_data


class ItemPedidoVendaForm(forms.ModelForm):
    class Meta:
        model = ItemPedidoVenda
        fields = [
            'produto', 'quantidade', 'preco_unitario', 'percentual_desconto',
            'observacoes'
        ]
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'percentual_desconto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        if quantidade <= 0:
            raise ValidationError('A quantidade deve ser maior que zero.')
        return quantidade

    def clean_preco_unitario(self):
        preco_unitario = self.cleaned_data['preco_unitario']
        if preco_unitario <= 0:
            raise ValidationError('O preço unitário deve ser maior que zero.')
        return preco_unitario


class ComissaoVendedorForm(forms.ModelForm):
    class Meta:
        model = ComissaoVendedor
        fields = [
            'vendedor', 'pedido_venda', 'valor_venda', 'percentual_comissao',
            'data_vencimento', 'observacoes'
        ]
        widgets = {
            'vendedor': forms.Select(attrs={'class': 'form-control'}),
            'pedido_venda': forms.Select(attrs={'class': 'form-control'}),
            'valor_venda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'percentual_comissao': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_valor_venda(self):
        valor_venda = self.cleaned_data['valor_venda']
        if valor_venda <= 0:
            raise ValidationError('O valor da venda deve ser maior que zero.')
        return valor_venda

    def clean_percentual_comissao(self):
        percentual_comissao = self.cleaned_data['percentual_comissao']
        if percentual_comissao < 0 or percentual_comissao > 100:
            raise ValidationError('O percentual de comissão deve estar entre 0 e 100.')
        return percentual_comissao


class MetaVendedorForm(forms.ModelForm):
    class Meta:
        model = MetaVendedor
        fields = [
            'vendedor', 'ano', 'mes', 'meta_valor', 'meta_quantidade'
        ]
        widgets = {
            'vendedor': forms.Select(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'mes': forms.Select(
                choices=[(i, f'{i:02d}') for i in range(1, 13)],
                attrs={'class': 'form-control'}
            ),
            'meta_valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'meta_quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_ano(self):
        ano = self.cleaned_data['ano']
        if ano < 2020 or ano > 2030:
            raise ValidationError('O ano deve estar entre 2020 e 2030.')
        return ano

    def clean_mes(self):
        mes = self.cleaned_data['mes']
        if mes < 1 or mes > 12:
            raise ValidationError('O mês deve estar entre 1 e 12.')
        return mes

    def clean_meta_valor(self):
        meta_valor = self.cleaned_data['meta_valor']
        if meta_valor <= 0:
            raise ValidationError('A meta de valor deve ser maior que zero.')
        return meta_valor

    def clean_meta_quantidade(self):
        meta_quantidade = self.cleaned_data['meta_quantidade']
        if meta_quantidade <= 0:
            raise ValidationError('A meta de quantidade deve ser maior que zero.')
        return meta_quantidade

    def clean(self):
        cleaned_data = super().clean()
        vendedor = cleaned_data.get('vendedor')
        ano = cleaned_data.get('ano')
        mes = cleaned_data.get('mes')
        
        if vendedor and ano and mes:
            if MetaVendedor.objects.filter(
                vendedor=vendedor, 
                ano=ano, 
                mes=mes
            ).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Já existe uma meta para este vendedor neste período.')
        
        return cleaned_data


# Formulários para filtros de relatórios
class RelatorioVendasForm(forms.Form):
    vendedor = forms.ModelChoiceField(
        queryset=Vendedor.objects.filter(ativo=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Todos os vendedores"
    )
    ano = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=2024
    )
    mes = forms.ChoiceField(
        choices=[('', 'Todos os meses')] + [(i, f'{i:02d}') for i in range(1, 13)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class RelatorioProdutosForm(forms.Form):
    ano = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=2024
    )
    mes = forms.ChoiceField(
        choices=[('', 'Todos os meses')] + [(i, f'{i:02d}') for i in range(1, 13)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    categoria = forms.ModelChoiceField(
        queryset=None,  # Será definido na view
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Todas as categorias"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from cadastros.models import CategoriaProduto
        self.fields['categoria'].queryset = CategoriaProduto.objects.filter(ativo=True)

