from django.db import models
from django.contrib.auth.models import User
from cadastros.models import Cliente, Produto, Vendedor, FormaPagamento


class StatusOrcamento(models.Model):
    """Status dos orçamentos"""
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código")
    descricao = models.CharField(max_length=100, verbose_name="Descrição")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Status de Orçamento"
        verbose_name_plural = "Status de Orçamentos"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class StatusPedido(models.Model):
    """Status dos pedidos de venda"""
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código")
    descricao = models.CharField(max_length=100, verbose_name="Descrição")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Status de Pedido"
        verbose_name_plural = "Status de Pedidos"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class Orcamento(models.Model):
    """Orçamentos de venda"""
    numero = models.CharField(max_length=20, unique=True, verbose_name="Número")
    data_orcamento = models.DateField(verbose_name="Data do Orçamento")
    data_validade = models.DateField(verbose_name="Data de Validade")
    
    # Cliente e vendedor
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, verbose_name="Vendedor")
    
    # Status e forma de pagamento
    status = models.ForeignKey(StatusOrcamento, on_delete=models.CASCADE, verbose_name="Status")
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, verbose_name="Forma de Pagamento")
    
    # Valores
    valor_produtos = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor dos Produtos")
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor do Desconto")
    percentual_desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Percentual de Desconto")
    valor_frete = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor do Frete")
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor Total")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    observacoes_internas = models.TextField(blank=True, null=True, verbose_name="Observações Internas")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    usuario_criacao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Criação")

    class Meta:
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"
        ordering = ['-data_orcamento', '-numero']

    def __str__(self):
        return f"Orçamento {self.numero} - {self.cliente.nome_razao_social}"

    def save(self, *args, **kwargs):
        # Calcular valor total
        self.valor_total = self.valor_produtos - self.valor_desconto + self.valor_frete
        super().save(*args, **kwargs)


class ItemOrcamento(models.Model):
    """Itens do orçamento"""
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name='itens', verbose_name="Orçamento")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    quantidade = models.DecimalField(max_digits=15, decimal_places=3, verbose_name="Quantidade")
    preco_unitario = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Preço Unitário")
    percentual_desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Desconto (%)")
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor do Desconto")
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor Total")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Item de Orçamento"
        verbose_name_plural = "Itens de Orçamento"
        ordering = ['orcamento', 'produto']

    def __str__(self):
        return f"{self.orcamento.numero} - {self.produto.descricao}"

    def save(self, *args, **kwargs):
        # Calcular valores
        valor_bruto = self.quantidade * self.preco_unitario
        self.valor_desconto = valor_bruto * (self.percentual_desconto / 100)
        self.valor_total = valor_bruto - self.valor_desconto
        super().save(*args, **kwargs)


class PedidoVenda(models.Model):
    """Pedidos de venda"""
    numero = models.CharField(max_length=20, unique=True, verbose_name="Número")
    data_pedido = models.DateField(verbose_name="Data do Pedido")
    data_entrega_prevista = models.DateField(verbose_name="Data de Entrega Prevista")
    data_entrega_realizada = models.DateField(blank=True, null=True, verbose_name="Data de Entrega Realizada")
    
    # Cliente e vendedor
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, verbose_name="Vendedor")
    
    # Referência ao orçamento (se houver)
    orcamento = models.ForeignKey(Orcamento, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Orçamento")
    
    # Status e forma de pagamento
    status = models.ForeignKey(StatusPedido, on_delete=models.CASCADE, verbose_name="Status")
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, verbose_name="Forma de Pagamento")
    
    # Valores
    valor_produtos = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor dos Produtos")
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor do Desconto")
    percentual_desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Percentual de Desconto")
    valor_frete = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor do Frete")
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor Total")
    
    # Comissão
    percentual_comissao = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Percentual de Comissão")
    valor_comissao = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor da Comissão")
    comissao_paga = models.BooleanField(default=False, verbose_name="Comissão Paga")
    data_pagamento_comissao = models.DateField(blank=True, null=True, verbose_name="Data de Pagamento da Comissão")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    observacoes_internas = models.TextField(blank=True, null=True, verbose_name="Observações Internas")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    usuario_criacao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Criação")

    class Meta:
        verbose_name = "Pedido de Venda"
        verbose_name_plural = "Pedidos de Venda"
        ordering = ['-data_pedido', '-numero']

    def __str__(self):
        return f"Pedido {self.numero} - {self.cliente.nome_razao_social}"

    def save(self, *args, **kwargs):
        # Calcular valores
        self.valor_total = self.valor_produtos - self.valor_desconto + self.valor_frete
        self.valor_comissao = self.valor_total * (self.percentual_comissao / 100)
        super().save(*args, **kwargs)


class ItemPedidoVenda(models.Model):
    """Itens do pedido de venda"""
    pedido = models.ForeignKey(PedidoVenda, on_delete=models.CASCADE, related_name='itens', verbose_name="Pedido")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    quantidade = models.DecimalField(max_digits=15, decimal_places=3, verbose_name="Quantidade")
    quantidade_entregue = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Quantidade Entregue")
    preco_unitario = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Preço Unitário")
    percentual_desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Desconto (%)")
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor do Desconto")
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor Total")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Item de Pedido de Venda"
        verbose_name_plural = "Itens de Pedido de Venda"
        ordering = ['pedido', 'produto']

    def __str__(self):
        return f"{self.pedido.numero} - {self.produto.descricao}"

    def save(self, *args, **kwargs):
        # Calcular valores
        valor_bruto = self.quantidade * self.preco_unitario
        self.valor_desconto = valor_bruto * (self.percentual_desconto / 100)
        self.valor_total = valor_bruto - self.valor_desconto
        super().save(*args, **kwargs)


class ComissaoVendedor(models.Model):
    """Controle de comissões dos vendedores"""
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, verbose_name="Vendedor")
    pedido_venda = models.ForeignKey(PedidoVenda, on_delete=models.CASCADE, verbose_name="Pedido de Venda")
    
    # Valores
    valor_venda = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor da Venda")
    percentual_comissao = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Percentual de Comissão")
    valor_comissao = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor da Comissão")
    
    # Controle de pagamento
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    data_pagamento = models.DateField(blank=True, null=True, verbose_name="Data de Pagamento")
    pago = models.BooleanField(default=False, verbose_name="Pago")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    usuario_criacao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Criação")

    class Meta:
        verbose_name = "Comissão de Vendedor"
        verbose_name_plural = "Comissões de Vendedores"
        ordering = ['-data_vencimento', 'vendedor']
        unique_together = ['vendedor', 'pedido_venda']

    def __str__(self):
        return f"Comissão {self.vendedor.nome} - Pedido {self.pedido_venda.numero}"

    def save(self, *args, **kwargs):
        # Calcular valor da comissão
        self.valor_comissao = self.valor_venda * (self.percentual_comissao / 100)
        super().save(*args, **kwargs)


class MetaVendedor(models.Model):
    """Metas dos vendedores por período"""
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, verbose_name="Vendedor")
    ano = models.IntegerField(verbose_name="Ano")
    mes = models.IntegerField(verbose_name="Mês")
    
    # Metas
    meta_valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Meta de Valor")
    meta_quantidade = models.IntegerField(default=0, verbose_name="Meta de Quantidade de Vendas")
    
    # Realizados
    realizado_valor = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor Realizado")
    realizado_quantidade = models.IntegerField(default=0, verbose_name="Quantidade Realizada")
    
    # Percentuais
    percentual_valor = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Percentual de Valor (%)")
    percentual_quantidade = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Percentual de Quantidade (%)")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        verbose_name = "Meta de Vendedor"
        verbose_name_plural = "Metas de Vendedores"
        ordering = ['-ano', '-mes', 'vendedor']
        unique_together = ['vendedor', 'ano', 'mes']

    def __str__(self):
        return f"Meta {self.vendedor.nome} - {self.mes:02d}/{self.ano}"

    def save(self, *args, **kwargs):
        # Calcular percentuais
        if self.meta_valor > 0:
            self.percentual_valor = (self.realizado_valor / self.meta_valor) * 100
        if self.meta_quantidade > 0:
            self.percentual_quantidade = (self.realizado_quantidade / self.meta_quantidade) * 100
        super().save(*args, **kwargs)

