from django import forms
from django.core.exceptions import ValidationError
from .models import (
    PlanoContas, CentroCusto, ContasPagar, ContasReceber, FluxoCaixa,
    LancamentoContabil, ItemLancamentoContabil, DRE, TipoConta
)
from cadastros.models import Cliente, Fornecedor, FormaPagamento


class PlanoContasForm(forms.ModelForm):
    class Meta:
        model = PlanoContas
        fields = [
            'codigo', 'descricao', 'conta_pai', 'tipo_conta', 'nivel',
            'aceita_lancamento'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'conta_pai': forms.Select(attrs={'class': 'form-control'}),
            'tipo_conta': forms.Select(attrs={'class': 'form-control'}),
            'nivel': forms.NumberInput(attrs={'class': 'form-control'}),
            'aceita_lancamento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if PlanoContas.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe uma conta com este código.')
        return codigo

    def clean_nivel(self):
        nivel = self.cleaned_data['nivel']
        if nivel < 1 or nivel > 10:
            raise ValidationError('O nível deve estar entre 1 e 10.')
        return nivel


class CentroCustoForm(forms.ModelForm):
    class Meta:
        model = CentroCusto
        fields = ['codigo', 'descricao', 'centro_pai', 'responsavel']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'centro_pai': forms.Select(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if CentroCusto.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe um centro de custo com este código.')
        return codigo


class ContasPagarForm(forms.ModelForm):
    class Meta:
        model = ContasPagar
        fields = [
            'numero', 'fornecedor', 'conta_contabil', 'centro_custo',
            'forma_pagamento', 'data_emissao', 'data_vencimento',
            'valor_original', 'valor_desconto', 'valor_juros', 'valor_multa',
            'numero_documento', 'tipo_documento', 'observacoes'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'conta_contabil': forms.Select(attrs={'class': 'form-control'}),
            'centro_custo': forms.Select(attrs={'class': 'form-control'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'data_emissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_original': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_desconto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_juros': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_multa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if ContasPagar.objects.filter(numero=numero).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe uma conta a pagar com este número.')
        return numero

    def clean_valor_original(self):
        valor_original = self.cleaned_data['valor_original']
        if valor_original <= 0:
            raise ValidationError('O valor original deve ser maior que zero.')
        return valor_original

    def clean(self):
        cleaned_data = super().clean()
        data_emissao = cleaned_data.get('data_emissao')
        data_vencimento = cleaned_data.get('data_vencimento')
        
        if data_emissao and data_vencimento:
            if data_vencimento < data_emissao:
                raise ValidationError('A data de vencimento deve ser posterior à data de emissão.')
        
        return cleaned_data


class ContasReceberForm(forms.ModelForm):
    class Meta:
        model = ContasReceber
        fields = [
            'numero', 'cliente', 'conta_contabil', 'centro_custo',
            'forma_pagamento', 'pedido_venda', 'data_emissao', 'data_vencimento',
            'valor_original', 'valor_desconto', 'valor_juros', 'valor_multa',
            'numero_documento', 'tipo_documento', 'observacoes'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'conta_contabil': forms.Select(attrs={'class': 'form-control'}),
            'centro_custo': forms.Select(attrs={'class': 'form-control'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'pedido_venda': forms.Select(attrs={'class': 'form-control'}),
            'data_emissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_original': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_desconto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_juros': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_multa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if ContasReceber.objects.filter(numero=numero).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe uma conta a receber com este número.')
        return numero

    def clean_valor_original(self):
        valor_original = self.cleaned_data['valor_original']
        if valor_original <= 0:
            raise ValidationError('O valor original deve ser maior que zero.')
        return valor_original

    def clean(self):
        cleaned_data = super().clean()
        data_emissao = cleaned_data.get('data_emissao')
        data_vencimento = cleaned_data.get('data_vencimento')
        
        if data_emissao and data_vencimento:
            if data_vencimento < data_emissao:
                raise ValidationError('A data de vencimento deve ser posterior à data de emissão.')
        
        return cleaned_data


class FluxoCaixaForm(forms.ModelForm):
    class Meta:
        model = FluxoCaixa
        fields = [
            'data_movimento', 'conta_contabil', 'centro_custo', 'tipo_movimento',
            'valor', 'descricao', 'numero_documento', 'observacoes'
        ]
        widgets = {
            'data_movimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'conta_contabil': forms.Select(attrs={'class': 'form-control'}),
            'centro_custo': forms.Select(attrs={'class': 'form-control'}),
            'tipo_movimento': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_valor(self):
        valor = self.cleaned_data['valor']
        if valor <= 0:
            raise ValidationError('O valor deve ser maior que zero.')
        return valor


class LancamentoContabilForm(forms.ModelForm):
    class Meta:
        model = LancamentoContabil
        fields = [
            'numero', 'data_lancamento', 'historico', 'valor_total'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'data_lancamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'historico': forms.TextInput(attrs={'class': 'form-control'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def clean_numero(self):
        numero = self.cleaned_data['numero']
        if LancamentoContabil.objects.filter(numero=numero).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe um lançamento com este número.')
        return numero

    def clean_valor_total(self):
        valor_total = self.cleaned_data['valor_total']
        if valor_total <= 0:
            raise ValidationError('O valor total deve ser maior que zero.')
        return valor_total


class ItemLancamentoContabilForm(forms.ModelForm):
    class Meta:
        model = ItemLancamentoContabil
        fields = [
            'conta_contabil', 'centro_custo', 'tipo', 'valor',
            'historico_complementar'
        ]
        widgets = {
            'conta_contabil': forms.Select(attrs={'class': 'form-control'}),
            'centro_custo': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'historico_complementar': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_valor(self):
        valor = self.cleaned_data['valor']
        if valor <= 0:
            raise ValidationError('O valor deve ser maior que zero.')
        return valor


class DREForm(forms.ModelForm):
    class Meta:
        model = DRE
        fields = [
            'ano', 'mes', 'receita_bruta', 'deducoes_receita',
            'custo_produtos_vendidos', 'despesas_vendas', 'despesas_administrativas',
            'despesas_financeiras', 'receitas_financeiras', 'outras_receitas',
            'outras_despesas', 'imposto_renda'
        ]
        widgets = {
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'mes': forms.Select(
                choices=[(i, f'{i:02d}') for i in range(1, 13)],
                attrs={'class': 'form-control'}
            ),
            'receita_bruta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'deducoes_receita': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'custo_produtos_vendidos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'despesas_vendas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'despesas_administrativas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'despesas_financeiras': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'receitas_financeiras': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'outras_receitas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'outras_despesas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'imposto_renda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
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

    def clean(self):
        cleaned_data = super().clean()
        ano = cleaned_data.get('ano')
        mes = cleaned_data.get('mes')
        
        if ano and mes:
            if DRE.objects.filter(ano=ano, mes=mes).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Já existe uma DRE para este período.')
        
        return cleaned_data


class TipoContaForm(forms.ModelForm):
    class Meta:
        model = TipoConta
        fields = ['codigo', 'descricao', 'natureza']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'natureza': forms.Select(attrs={'class': 'form-control'}),
        }


# Formulários para filtros de relatórios
class RelatorioContasForm(forms.Form):
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    status = forms.ChoiceField(
        choices=[('', 'Todos')] + [
            ('ABERTO', 'Aberto'),
            ('PAGO', 'Pago'),
            ('VENCIDO', 'Vencido'),
            ('CANCELADO', 'Cancelado')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class RelatorioFluxoCaixaForm(forms.Form):
    data_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    data_fim = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    centro_custo = forms.ModelChoiceField(
        queryset=CentroCusto.objects.filter(ativo=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Todos os centros de custo"
    )
    tipo_movimento = forms.ChoiceField(
        choices=[('', 'Todos')] + [('ENTRADA', 'Entrada'), ('SAIDA', 'Saída')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class RelatorioDREForm(forms.Form):
    ano = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial=2024
    )
    mes_inicio = forms.ChoiceField(
        choices=[(i, f'{i:02d}') for i in range(1, 13)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=1
    )
    mes_fim = forms.ChoiceField(
        choices=[(i, f'{i:02d}') for i in range(1, 13)],
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=12
    )

