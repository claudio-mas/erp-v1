from django.db import models
from django.contrib.auth.models import User
from cadastros.models import Produto, Fornecedor
from vendas.models import PedidoVenda, ItemPedidoVenda


class TipoMovimentacao(models.Model):
    """Tipos de movimentação de estoque"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    descricao = models.CharField(max_length=100, verbose_name="Descrição")
    tipo = models.CharField(
        max_length=1, 
        choices=[('E', 'Entrada'), ('S', 'Saída')],
        verbose_name="Tipo"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Tipo de Movimentação"
        verbose_name_plural = "Tipos de Movimentação"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class LocalEstoque(models.Model):
    """Locais de estoque"""
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código")
    descricao = models.CharField(max_length=100, verbose_name="Descrição")
    endereco = models.CharField(max_length=200, blank=True, null=True, verbose_name="Endereço")
    responsavel = models.CharField(max_length=100, blank=True, null=True, verbose_name="Responsável")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    class Meta:
        verbose_name = "Local de Estoque"
        verbose_name_plural = "Locais de Estoque"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class MovimentacaoEstoque(models.Model):
    """Movimentações de estoque"""
    numero = models.CharField(max_length=20, unique=True, verbose_name="Número")
    data_movimentacao = models.DateTimeField(verbose_name="Data da Movimentação")
    
    # Produto e local
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    local_estoque = models.ForeignKey(LocalEstoque, on_delete=models.CASCADE, verbose_name="Local de Estoque")
    
    # Tipo de movimentação
    tipo_movimentacao = models.ForeignKey(TipoMovimentacao, on_delete=models.CASCADE, verbose_name="Tipo de Movimentação")
    
    # Quantidades
    quantidade = models.DecimalField(max_digits=15, decimal_places=3, verbose_name="Quantidade")
    quantidade_anterior = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Quantidade Anterior")
    quantidade_atual = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Quantidade Atual")
    
    # Valores
    custo_unitario = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Custo Unitário")
    custo_total = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Custo Total")
    
    # Referências
    pedido_venda = models.ForeignKey(PedidoVenda, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Pedido de Venda")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Fornecedor")
    documento_referencia = models.CharField(max_length=50, blank=True, null=True, verbose_name="Documento de Referência")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    usuario_criacao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Criação")

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao', '-numero']

    def __str__(self):
        return f"{self.numero} - {self.produto.descricao} - {self.tipo_movimentacao.descricao}"

    def save(self, *args, **kwargs):
        # Calcular custo total
        self.custo_total = self.quantidade * self.custo_unitario
        
        # Atualizar estoque do produto
        if self.tipo_movimentacao.tipo == 'E':  # Entrada
            self.quantidade_atual = self.quantidade_anterior + self.quantidade
        else:  # Saída
            self.quantidade_atual = self.quantidade_anterior - self.quantidade
        
        super().save(*args, **kwargs)
        
        # Atualizar estoque atual do produto
        self.produto.estoque_atual = self.quantidade_atual
        self.produto.save()


class EstoqueProduto(models.Model):
    """Estoque atual dos produtos por local"""
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    local_estoque = models.ForeignKey(LocalEstoque, on_delete=models.CASCADE, verbose_name="Local de Estoque")
    quantidade_atual = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Quantidade Atual")
    quantidade_reservada = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Quantidade Reservada")
    quantidade_disponivel = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Quantidade Disponível")
    custo_medio = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Custo Médio")
    data_ultima_movimentacao = models.DateTimeField(blank=True, null=True, verbose_name="Data da Última Movimentação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        verbose_name = "Estoque de Produto"
        verbose_name_plural = "Estoque de Produtos"
        ordering = ['produto', 'local_estoque']
        unique_together = ['produto', 'local_estoque']

    def __str__(self):
        return f"{self.produto.descricao} - {self.local_estoque.descricao}"

    def save(self, *args, **kwargs):
        # Calcular quantidade disponível
        self.quantidade_disponivel = self.quantidade_atual - self.quantidade_reservada
        super().save(*args, **kwargs)


class Inventario(models.Model):
    """Inventários de estoque"""
    numero = models.CharField(max_length=20, unique=True, verbose_name="Número")
    data_inventario = models.DateField(verbose_name="Data do Inventário")
    data_inicio = models.DateTimeField(verbose_name="Data de Início")
    data_fim = models.DateTimeField(blank=True, null=True, verbose_name="Data de Fim")
    
    # Local
    local_estoque = models.ForeignKey(LocalEstoque, on_delete=models.CASCADE, verbose_name="Local de Estoque")
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('PLANEJADO', 'Planejado'),
            ('EM_ANDAMENTO', 'Em Andamento'),
            ('CONCLUIDO', 'Concluído'),
            ('CANCELADO', 'Cancelado')
        ],
        default='PLANEJADO',
        verbose_name="Status"
    )
    
    # Responsável
    responsavel = models.CharField(max_length=100, verbose_name="Responsável")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Controle
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    usuario_criacao = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Criação")

    class Meta:
        verbose_name = "Inventário"
        verbose_name_plural = "Inventários"
        ordering = ['-data_inventario', '-numero']

    def __str__(self):
        return f"Inventário {self.numero} - {self.local_estoque.descricao}"


class ItemInventario(models.Model):
    """Itens do inventário"""
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name='itens', verbose_name="Inventário")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    
    # Quantidades
    quantidade_sistema = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Quantidade no Sistema")
    quantidade_contada = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Quantidade Contada")
    diferenca = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Diferença")
    
    # Valores
    custo_unitario = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Custo Unitário")
    valor_diferenca = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Valor da Diferença")
    
    # Status
    conferido = models.BooleanField(default=False, verbose_name="Conferido")
    ajustado = models.BooleanField(default=False, verbose_name="Ajustado")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Controle
    data_contagem = models.DateTimeField(blank=True, null=True, verbose_name="Data da Contagem")
    usuario_contagem = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Usuário da Contagem")

    class Meta:
        verbose_name = "Item de Inventário"
        verbose_name_plural = "Itens de Inventário"
        ordering = ['inventario', 'produto']
        unique_together = ['inventario', 'produto']

    def __str__(self):
        return f"{self.inventario.numero} - {self.produto.descricao}"

    def save(self, *args, **kwargs):
        # Calcular diferença e valor
        self.diferenca = self.quantidade_contada - self.quantidade_sistema
        self.valor_diferenca = self.diferenca * self.custo_unitario
        super().save(*args, **kwargs)


class ReservaProduto(models.Model):
    """Reservas de produtos para pedidos"""
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    local_estoque = models.ForeignKey(LocalEstoque, on_delete=models.CASCADE, verbose_name="Local de Estoque")
    pedido_venda = models.ForeignKey(PedidoVenda, on_delete=models.CASCADE, verbose_name="Pedido de Venda")
    item_pedido = models.ForeignKey(ItemPedidoVenda, on_delete=models.CASCADE, verbose_name="Item do Pedido")
    
    # Quantidades
    quantidade_reservada = models.DecimalField(max_digits=15, decimal_places=3, verbose_name="Quantidade Reservada")
    quantidade_liberada = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Quantidade Liberada")
    
    # Status
    ativa = models.BooleanField(default=True, verbose_name="Ativa")
    
    # Datas
    data_reserva = models.DateTimeField(auto_now_add=True, verbose_name="Data da Reserva")
    data_liberacao = models.DateTimeField(blank=True, null=True, verbose_name="Data da Liberação")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Controle
    usuario_reserva = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário da Reserva")

    class Meta:
        verbose_name = "Reserva de Produto"
        verbose_name_plural = "Reservas de Produtos"
        ordering = ['-data_reserva']

    def __str__(self):
        return f"Reserva {self.produto.descricao} - Pedido {self.pedido_venda.numero}"


class ProdutoFornecedor(models.Model):
    """Relacionamento entre produtos e fornecedores"""
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, verbose_name="Fornecedor")
    codigo_fornecedor = models.CharField(max_length=50, verbose_name="Código do Fornecedor")
    descricao_fornecedor = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descrição do Fornecedor")
    preco_compra = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Preço de Compra")
    prazo_entrega_dias = models.IntegerField(default=0, verbose_name="Prazo de Entrega (dias)")
    quantidade_minima = models.DecimalField(max_digits=15, decimal_places=3, default=1, verbose_name="Quantidade Mínima")
    fornecedor_principal = models.BooleanField(default=False, verbose_name="Fornecedor Principal")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_ultima_compra = models.DateField(blank=True, null=True, verbose_name="Data da Última Compra")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        verbose_name = "Produto x Fornecedor"
        verbose_name_plural = "Produtos x Fornecedores"
        ordering = ['produto', 'fornecedor']
        unique_together = ['produto', 'fornecedor']

    def __str__(self):
        return f"{self.produto.descricao} - {self.fornecedor.nome_razao_social}"
