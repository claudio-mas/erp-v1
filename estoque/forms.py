from django import forms
from django.core.exceptions import ValidationError
from .models import (
    MovimentacaoEstoque, Inventario, ItemInventario, ReservaProduto,
    ProdutoFornecedor, TipoMovimentacao, LocalEstoque
)
from cadastros.models import Produto, Fornecedor
from vendas.models import PedidoVenda, ItemPedidoVenda


class MovimentacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = [
            'numero', 'data_movimentacao', 'produto', 'local_estoque',
            'tipo_movimentacao', 'quantidade', 'custo_unitario',
            'fornecedor', 'documento_referencia', 'observacoes'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'data_movimentacao': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'local_estoque': forms.Select(attrs={'class': 'form-control'}),
            'tipo_movimentacao': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'custo_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'documento_referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if MovimentacaoEstoque.objects.filter(numero=numero).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe uma movimentação com este número.')
        return numero

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        if quantidade <= 0:
            raise ValidationError('A quantidade deve ser maior que zero.')
        return quantidade

    def clean_custo_unitario(self):
        custo_unitario = self.cleaned_data['custo_unitario']
        if custo_unitario < 0:
            raise ValidationError('O custo unitário não pode ser negativo.')
        return custo_unitario


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = [
            'numero', 'data_inventario', 'data_inicio', 'local_estoque',
            'status', 'responsavel', 'observacoes'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'data_inventario': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'local_estoque': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if Inventario.objects.filter(numero=numero).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe um inventário com este número.')
        return numero


class ItemInventarioForm(forms.ModelForm):
    class Meta:
        model = ItemInventario
        fields = [
            'produto', 'quantidade_sistema', 'quantidade_contada',
            'custo_unitario', 'observacoes'
        ]
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade_sistema': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'readonly': True}),
            'quantidade_contada': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'custo_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_quantidade_contada(self):
        quantidade_contada = self.cleaned_data['quantidade_contada']
        if quantidade_contada < 0:
            raise ValidationError('A quantidade contada não pode ser negativa.')
        return quantidade_contada

    def clean_custo_unitario(self):
        custo_unitario = self.cleaned_data['custo_unitario']
        if custo_unitario < 0:
            raise ValidationError('O custo unitário não pode ser negativo.')
        return custo_unitario


class ReservaProdutoForm(forms.ModelForm):
    class Meta:
        model = ReservaProduto
        fields = [
            'produto', 'local_estoque', 'pedido_venda', 'item_pedido',
            'quantidade_reservada', 'observacoes'
        ]
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'local_estoque': forms.Select(attrs={'class': 'form-control'}),
            'pedido_venda': forms.Select(attrs={'class': 'form-control'}),
            'item_pedido': forms.Select(attrs={'class': 'form-control'}),
            'quantidade_reservada': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_quantidade_reservada(self):
        quantidade_reservada = self.cleaned_data['quantidade_reservada']
        if quantidade_reservada <= 0:
            raise ValidationError('A quantidade reservada deve ser maior que zero.')
        return quantidade_reservada

    def clean(self):
        cleaned_data = super().clean()
        produto = cleaned_data.get('produto')
        local_estoque = cleaned_data.get('local_estoque')
        quantidade_reservada = cleaned_data.get('quantidade_reservada')
        
        if produto and local_estoque and quantidade_reservada:
            try:
                from .models import EstoqueProduto
                estoque = EstoqueProduto.objects.get(
                    produto=produto,
                    local_estoque=local_estoque
                )
                if quantidade_reservada > estoque.quantidade_disponivel:
                    raise ValidationError(
                        f'Quantidade indisponível. Disponível: {estoque.quantidade_disponivel}'
                    )
            except EstoqueProduto.DoesNotExist:
                raise ValidationError('Produto não possui estoque neste local.')
        
        return cleaned_data


class ProdutoFornecedorForm(forms.ModelForm):
    class Meta:
        model = ProdutoFornecedor
        fields = [
            'produto', 'fornecedor', 'codigo_fornecedor', 'descricao_fornecedor',
            'preco_compra', 'prazo_entrega_dias', 'quantidade_minima',
            'fornecedor_principal'
        ]
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'codigo_fornecedor': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_fornecedor': forms.TextInput(attrs={'class': 'form-control'}),
            'preco_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'prazo_entrega_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantidade_minima': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'fornecedor_principal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_preco_compra(self):
        preco_compra = self.cleaned_data['preco_compra']
        if preco_compra < 0:
            raise ValidationError('O preço de compra não pode ser negativo.')
        return preco_compra

    def clean_prazo_entrega_dias(self):
        prazo_entrega_dias = self.cleaned_data['prazo_entrega_dias']
        if prazo_entrega_dias < 0:
            raise ValidationError('O prazo de entrega não pode ser negativo.')
        return prazo_entrega_dias

    def clean_quantidade_minima(self):
        quantidade_minima = self.cleaned_data['quantidade_minima']
        if quantidade_minima <= 0:
            raise ValidationError('A quantidade mínima deve ser maior que zero.')
        return quantidade_minima

    def clean(self):
        cleaned_data = super().clean()
        produto = cleaned_data.get('produto')
        fornecedor = cleaned_data.get('fornecedor')
        
        if produto and fornecedor:
            if ProdutoFornecedor.objects.filter(
                produto=produto,
                fornecedor=fornecedor
            ).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Já existe um relacionamento entre este produto e fornecedor.')
        
        return cleaned_data


# Formulários para filtros de relatórios
class RelatorioEstoqueForm(forms.Form):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.filter(ativo=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Todos os produtos"
    )
    local_estoque = forms.ModelChoiceField(
        queryset=LocalEstoque.objects.filter(ativo=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Todos os locais"
    )
    estoque_baixo = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Apenas produtos com estoque baixo"
    )


class RelatorioMovimentacoesForm(forms.Form):
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    tipo_movimentacao = forms.ChoiceField(
        choices=[('', 'Todos')] + [('E', 'Entrada'), ('S', 'Saída')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.filter(ativo=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Todos os produtos"
    )
    local_estoque = forms.ModelChoiceField(
        queryset=LocalEstoque.objects.filter(ativo=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Todos os locais"
    )


class TipoMovimentacaoForm(forms.ModelForm):
    class Meta:
        model = TipoMovimentacao
        fields = ['codigo', 'descricao', 'tipo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }


class LocalEstoqueForm(forms.ModelForm):
    class Meta:
        model = LocalEstoque
        fields = ['codigo', 'descricao', 'endereco', 'responsavel']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
        }

