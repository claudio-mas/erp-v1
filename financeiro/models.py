from django.db import models
from django.contrib.auth.models import User
from cadastros.models import Cliente, Fornecedor, FormaPagamento
from vendas.models import PedidoVenda


class TipoConta(models.Model):
    """Tipos de conta do plano de contas"""
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código")
    descricao = models.CharField(max_length=100, verbose_name="Descrição")
    natureza = models.CharField(
        max_length=10,
        choices=[
            ('ATIVO', 'Ativo'),
            ('PASSIVO', 'Passivo'),
            ('RECEITA', 'Receita'),
            ('DESPESA', 'Despesa'),
            ('PATRIMONIO', 'Patrimônio Líquido')
        ],
        verbose_name="Natureza"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Tipo de Conta"
        verbose_name_plural = "Tipos de Conta"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class PlanoContas(models.Model):
    """Plano de contas"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    conta_pai = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Conta Pai")
    tipo_conta = models.ForeignKey(TipoConta, on_delete=models.CASCADE, verbose_name="Tipo de Conta")
    nivel = models.IntegerField(default=1, verbose_name="Nível")
    aceita_lancamento = models.BooleanField(default=True, verbose_name="Aceita Lançamento")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        verbose_name = "Plano de Contas"
        verbose_name_plural = "Plano de Contas"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class CentroCusto(models.Model):
    """Centros de custo"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    centro_pai = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Centro Pai")
    responsavel = models.CharField(max_length=100, blank=True, null=True, verbose_name="Responsável")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    class Meta:
        verbose_name = "Centro de Custo"
        verbose_name_plural = "Centros de Custo"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class ContasPagar(models.Model):
    """Contas a pagar"""
    numero = models.CharField(max_length=20, unique=True, verbose_name="Número")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, verbose_name="Fornecedor")
    conta_contabil = models.ForeignKey(PlanoContas, on_delete=models.CASCADE, verbose_name="Conta Contábil")
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.CASCADE, verbose_name="Centro de Custo")
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, verbose_name="Forma de Pagamento")
    
    # Datas
    data_emissao = models.DateField(verbose_name="Data de Emissão")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    data_pagamento = models.DateField(blank=True, null=True, verbose_name="Data de Pagamento")
    
    # Valores
    valor_original = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor Original")
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor do Desconto")
    valor_juros = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor dos Juros")
    valor_multa = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor da Multa")
    valor_pago = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor Pago")
    valor_saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor do Saldo")
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('ABERTO', 'Aberto'),
            ('PAGO', 'Pago'),
            ('VENCIDO', 'Vencido'),
            ('CANCELADO', 'Cancelado')
        ],
        default='ABERTO',
        verbose_name="Status"
    )
    
    # Documentos
    numero_documento = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número do Documento")
    tipo_documento = models.CharField(max_length=20, blank=True, null=True, verbose_name="Tipo de Documento")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    usuario_criacao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Criação")

    class Meta:
        verbose_name = "Conta a Pagar"
        verbose_name_plural = "Contas a Pagar"
        ordering = ['data_vencimento', 'fornecedor']

    def __str__(self):
        return f"{self.numero} - {self.fornecedor.nome_razao_social}"

    def save(self, *args, **kwargs):
        # Calcular saldo
        self.valor_saldo = self.valor_original + self.valor_juros + self.valor_multa - self.valor_desconto - self.valor_pago
        
        # Atualizar status
        if self.valor_saldo <= 0:
            self.status = 'PAGO'
        elif self.data_vencimento < models.DateField().today() and self.status == 'ABERTO':
            self.status = 'VENCIDO'
        
        super().save(*args, **kwargs)


class ContasReceber(models.Model):
    """Contas a receber"""
    numero = models.CharField(max_length=20, unique=True, verbose_name="Número")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    conta_contabil = models.ForeignKey(PlanoContas, on_delete=models.CASCADE, verbose_name="Conta Contábil")
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.CASCADE, verbose_name="Centro de Custo")
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, verbose_name="Forma de Pagamento")
    pedido_venda = models.ForeignKey(PedidoVenda, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Pedido de Venda")
    
    # Datas
    data_emissao = models.DateField(verbose_name="Data de Emissão")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    data_recebimento = models.DateField(blank=True, null=True, verbose_name="Data de Recebimento")
    
    # Valores
    valor_original = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor Original")
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor do Desconto")
    valor_juros = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor dos Juros")
    valor_multa = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor da Multa")
    valor_recebido = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor Recebido")
    valor_saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor do Saldo")
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('ABERTO', 'Aberto'),
            ('RECEBIDO', 'Recebido'),
            ('VENCIDO', 'Vencido'),
            ('CANCELADO', 'Cancelado')
        ],
        default='ABERTO',
        verbose_name="Status"
    )
    
    # Documentos
    numero_documento = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número do Documento")
    tipo_documento = models.CharField(max_length=20, blank=True, null=True, verbose_name="Tipo de Documento")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    usuario_criacao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Criação")

    class Meta:
        verbose_name = "Conta a Receber"
        verbose_name_plural = "Contas a Receber"
        ordering = ['data_vencimento', 'cliente']

    def __str__(self):
        return f"{self.numero} - {self.cliente.nome_razao_social}"

    def save(self, *args, **kwargs):
        # Calcular saldo
        self.valor_saldo = self.valor_original + self.valor_juros + self.valor_multa - self.valor_desconto - self.valor_recebido
        
        # Atualizar status
        if self.valor_saldo <= 0:
            self.status = 'RECEBIDO'
        elif self.data_vencimento < models.DateField().today() and self.status == 'ABERTO':
            self.status = 'VENCIDO'
        
        super().save(*args, **kwargs)


class FluxoCaixa(models.Model):
    """Fluxo de caixa"""
    data_movimento = models.DateField(verbose_name="Data do Movimento")
    conta_contabil = models.ForeignKey(PlanoContas, on_delete=models.CASCADE, verbose_name="Conta Contábil")
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.CASCADE, verbose_name="Centro de Custo")
    
    # Tipo de movimento
    tipo_movimento = models.CharField(
        max_length=10,
        choices=[
            ('ENTRADA', 'Entrada'),
            ('SAIDA', 'Saída')
        ],
        verbose_name="Tipo de Movimento"
    )
    
    # Valores
    valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor")
    
    # Origem
    conta_pagar = models.ForeignKey(ContasPagar, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Conta a Pagar")
    conta_receber = models.ForeignKey(ContasReceber, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Conta a Receber")
    
    # Descrição
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Documentos
    numero_documento = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número do Documento")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    usuario_criacao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Criação")

    class Meta:
        verbose_name = "Fluxo de Caixa"
        verbose_name_plural = "Fluxo de Caixa"
        ordering = ['-data_movimento']

    def __str__(self):
        return f"{self.data_movimento} - {self.descricao} - R$ {self.valor}"


class LancamentoContabil(models.Model):
    """Lançamentos contábeis"""
    numero = models.CharField(max_length=20, unique=True, verbose_name="Número")
    data_lancamento = models.DateField(verbose_name="Data do Lançamento")
    historico = models.CharField(max_length=200, verbose_name="Histórico")
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor Total")
    
    # Origem
    conta_pagar = models.ForeignKey(ContasPagar, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Conta a Pagar")
    conta_receber = models.ForeignKey(ContasReceber, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Conta a Receber")
    pedido_venda = models.ForeignKey(PedidoVenda, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Pedido de Venda")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    usuario_criacao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Criação")

    class Meta:
        verbose_name = "Lançamento Contábil"
        verbose_name_plural = "Lançamentos Contábeis"
        ordering = ['-data_lancamento', '-numero']

    def __str__(self):
        return f"{self.numero} - {self.historico}"


class ItemLancamentoContabil(models.Model):
    """Itens dos lançamentos contábeis"""
    lancamento = models.ForeignKey(LancamentoContabil, on_delete=models.CASCADE, related_name='itens', verbose_name="Lançamento")
    conta_contabil = models.ForeignKey(PlanoContas, on_delete=models.CASCADE, verbose_name="Conta Contábil")
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.CASCADE, verbose_name="Centro de Custo")
    
    # Tipo de lançamento
    tipo = models.CharField(
        max_length=10,
        choices=[
            ('DEBITO', 'Débito'),
            ('CREDITO', 'Crédito')
        ],
        verbose_name="Tipo"
    )
    
    # Valor
    valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor")
    
    # Histórico complementar
    historico_complementar = models.CharField(max_length=200, blank=True, null=True, verbose_name="Histórico Complementar")

    class Meta:
        verbose_name = "Item de Lançamento Contábil"
        verbose_name_plural = "Itens de Lançamento Contábil"
        ordering = ['lancamento', 'tipo', 'conta_contabil']

    def __str__(self):
        return f"{self.lancamento.numero} - {self.conta_contabil.descricao} - {self.tipo}"


class DRE(models.Model):
    """Demonstração do Resultado do Exercício"""
    ano = models.IntegerField(verbose_name="Ano")
    mes = models.IntegerField(verbose_name="Mês")
    
    # Receitas
    receita_bruta = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Receita Bruta")
    deducoes_receita = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Deduções da Receita")
    receita_liquida = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Receita Líquida")
    
    # Custos
    custo_produtos_vendidos = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Custo dos Produtos Vendidos")
    lucro_bruto = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Lucro Bruto")
    
    # Despesas operacionais
    despesas_vendas = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Despesas de Vendas")
    despesas_administrativas = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Despesas Administrativas")
    despesas_financeiras = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Despesas Financeiras")
    receitas_financeiras = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Receitas Financeiras")
    
    # Resultado
    resultado_operacional = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Resultado Operacional")
    outras_receitas = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Outras Receitas")
    outras_despesas = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Outras Despesas")
    resultado_antes_ir = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Resultado Antes do IR")
    imposto_renda = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Imposto de Renda")
    resultado_liquido = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Resultado Líquido")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    usuario_criacao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Criação")

    class Meta:
        verbose_name = "DRE"
        verbose_name_plural = "DREs"
        ordering = ['-ano', '-mes']
        unique_together = ['ano', 'mes']

    def __str__(self):
        return f"DRE {self.mes:02d}/{self.ano}"

    def save(self, *args, **kwargs):
        # Calcular valores derivados
        self.receita_liquida = self.receita_bruta - self.deducoes_receita
        self.lucro_bruto = self.receita_liquida - self.custo_produtos_vendidos
        self.resultado_operacional = (self.lucro_bruto - self.despesas_vendas - 
                                    self.despesas_administrativas - self.despesas_financeiras + 
                                    self.receitas_financeiras)
        self.resultado_antes_ir = self.resultado_operacional + self.outras_receitas - self.outras_despesas
        self.resultado_liquido = self.resultado_antes_ir - self.imposto_renda
        super().save(*args, **kwargs)

