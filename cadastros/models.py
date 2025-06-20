from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class TabelaAuxiliar(models.Model):
    """Modelo base para tabelas auxiliares do sistema"""
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código")
    descricao = models.CharField(max_length=100, verbose_name="Descrição")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        abstract = True
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class Estado(TabelaAuxiliar):
    """Estados do Brasil"""
    sigla = models.CharField(max_length=2, unique=True, verbose_name="Sigla")

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"


class Cidade(models.Model):
    """Cidades"""
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código")
    nome = models.CharField(max_length=100, verbose_name="Nome")
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="Estado")
    codigo_ibge = models.CharField(max_length=10, blank=True, null=True, verbose_name="Código IBGE")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.estado.sigla}"


class TipoPessoa(TabelaAuxiliar):
    """Tipos de pessoa (Física, Jurídica)"""
    
    class Meta:
        verbose_name = "Tipo de Pessoa"
        verbose_name_plural = "Tipos de Pessoa"


class SegmentoMercado(TabelaAuxiliar):
    """Segmentos de mercado"""
    
    class Meta:
        verbose_name = "Segmento de Mercado"
        verbose_name_plural = "Segmentos de Mercado"


class FormaPagamento(TabelaAuxiliar):
    """Formas de pagamento"""
    prazo_dias = models.IntegerField(default=0, verbose_name="Prazo em Dias")
    
    class Meta:
        verbose_name = "Forma de Pagamento"
        verbose_name_plural = "Formas de Pagamento"


class Cliente(models.Model):
    """Cadastro de clientes"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    nome_razao_social = models.CharField(max_length=200, verbose_name="Nome/Razão Social")
    nome_fantasia = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nome Fantasia")
    tipo_pessoa = models.ForeignKey(TipoPessoa, on_delete=models.CASCADE, verbose_name="Tipo de Pessoa")
    
    # Documentos
    cpf_cnpj = models.CharField(
        max_length=18, 
        unique=True, 
        verbose_name="CPF/CNPJ",
        validators=[RegexValidator(
            regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
            message='CPF deve estar no formato XXX.XXX.XXX-XX ou CNPJ no formato XX.XXX.XXX/XXXX-XX'
        )]
    )
    rg_ie = models.CharField(max_length=20, blank=True, null=True, verbose_name="RG/IE")
    
    # Endereço
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cep = models.CharField(max_length=10, verbose_name="CEP")
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, verbose_name="Cidade")
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    celular = models.CharField(max_length=20, blank=True, null=True, verbose_name="Celular")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    site = models.URLField(blank=True, null=True, verbose_name="Site")
    
    # Informações comerciais
    segmento_mercado = models.ForeignKey(SegmentoMercado, on_delete=models.CASCADE, verbose_name="Segmento de Mercado")
    forma_pagamento_padrao = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, verbose_name="Forma de Pagamento Padrão")
    limite_credito = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Limite de Crédito")
    
    # Controle
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    usuario_cadastro = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Cadastro")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome_razao_social']

    def __str__(self):
        return f"{self.codigo} - {self.nome_razao_social}"


class Fornecedor(models.Model):
    """Cadastro de fornecedores"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    nome_razao_social = models.CharField(max_length=200, verbose_name="Nome/Razão Social")
    nome_fantasia = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nome Fantasia")
    tipo_pessoa = models.ForeignKey(TipoPessoa, on_delete=models.CASCADE, verbose_name="Tipo de Pessoa")
    
    # Documentos
    cpf_cnpj = models.CharField(
        max_length=18, 
        unique=True, 
        verbose_name="CPF/CNPJ",
        validators=[RegexValidator(
            regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
            message='CPF deve estar no formato XXX.XXX.XXX-XX ou CNPJ no formato XX.XXX.XXX/XXXX-XX'
        )]
    )
    rg_ie = models.CharField(max_length=20, blank=True, null=True, verbose_name="RG/IE")
    
    # Endereço
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cep = models.CharField(max_length=10, verbose_name="CEP")
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, verbose_name="Cidade")
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    celular = models.CharField(max_length=20, blank=True, null=True, verbose_name="Celular")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    site = models.URLField(blank=True, null=True, verbose_name="Site")
    
    # Informações comerciais
    forma_pagamento_padrao = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, verbose_name="Forma de Pagamento Padrão")
    prazo_entrega_dias = models.IntegerField(default=0, verbose_name="Prazo de Entrega (dias)")
    
    # Dados bancários
    banco = models.CharField(max_length=100, blank=True, null=True, verbose_name="Banco")
    agencia = models.CharField(max_length=20, blank=True, null=True, verbose_name="Agência")
    conta = models.CharField(max_length=20, blank=True, null=True, verbose_name="Conta")
    
    # Controle
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    usuario_cadastro = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Cadastro")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome_razao_social']

    def __str__(self):
        return f"{self.codigo} - {self.nome_razao_social}"


class UnidadeMedida(TabelaAuxiliar):
    """Unidades de medida"""
    sigla = models.CharField(max_length=5, unique=True, verbose_name="Sigla")
    
    class Meta:
        verbose_name = "Unidade de Medida"
        verbose_name_plural = "Unidades de Medida"


class CategoriaProduto(TabelaAuxiliar):
    """Categorias de produtos"""
    categoria_pai = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Categoria Pai")
    
    class Meta:
        verbose_name = "Categoria de Produto"
        verbose_name_plural = "Categorias de Produto"


class Produto(models.Model):
    """Cadastro de produtos"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    codigo_barras = models.CharField(max_length=20, blank=True, null=True, verbose_name="Código de Barras")
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    descricao_detalhada = models.TextField(blank=True, null=True, verbose_name="Descrição Detalhada")
    
    # Classificação
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.CASCADE, verbose_name="Categoria")
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete=models.CASCADE, verbose_name="Unidade de Medida")
    
    # Preços e custos
    preco_custo = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Preço de Custo")
    preco_venda = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Preço de Venda")
    margem_lucro = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Margem de Lucro (%)")
    
    # Estoque
    estoque_minimo = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Estoque Mínimo")
    estoque_maximo = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Estoque Máximo")
    estoque_atual = models.DecimalField(max_digits=15, decimal_places=3, default=0, verbose_name="Estoque Atual")
    
    # Dimensões e peso
    peso = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Peso (kg)")
    altura = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Altura (cm)")
    largura = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Largura (cm)")
    profundidade = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Profundidade (cm)")
    
    # Fornecedor padrão
    fornecedor_padrao = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Fornecedor Padrão")
    
    # Controle
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    usuario_cadastro = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Cadastro")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['descricao']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class Vendedor(models.Model):
    """Cadastro de vendedores"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    nome = models.CharField(max_length=200, verbose_name="Nome")
    cpf = models.CharField(
        max_length=14, 
        unique=True, 
        verbose_name="CPF",
        validators=[RegexValidator(
            regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
            message='CPF deve estar no formato XXX.XXX.XXX-XX'
        )]
    )
    rg = models.CharField(max_length=20, verbose_name="RG")
    
    # Endereço
    endereco = models.CharField(max_length=200, verbose_name="Endereço")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cep = models.CharField(max_length=10, verbose_name="CEP")
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, verbose_name="Cidade")
    
    # Contato
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    celular = models.CharField(max_length=20, verbose_name="Celular")
    email = models.EmailField(verbose_name="E-mail")
    
    # Informações profissionais
    data_admissao = models.DateField(verbose_name="Data de Admissão")
    data_demissao = models.DateField(blank=True, null=True, verbose_name="Data de Demissão")
    salario_base = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Salário Base")
    comissao_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Comissão (%)")
    meta_mensal = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Meta Mensal")
    
    # Dados bancários
    banco = models.CharField(max_length=100, blank=True, null=True, verbose_name="Banco")
    agencia = models.CharField(max_length=20, blank=True, null=True, verbose_name="Agência")
    conta = models.CharField(max_length=20, blank=True, null=True, verbose_name="Conta")
    
    # Controle
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    usuario_cadastro = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário de Cadastro")
    
    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"
        ordering = ['nome']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
