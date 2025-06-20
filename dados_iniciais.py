#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from cadastros.models import (
    Estado, Cidade, TipoPessoa, SegmentoMercado, FormaPagamento,
    UnidadeMedida, CategoriaProduto
)
from estoque.models import TipoMovimentacao, LocalEstoque
from financeiro.models import TipoConta, CentroCusto

def criar_dados_iniciais():
    print("Criando dados iniciais...")
    
    # Verificar se já existem dados
    if Estado.objects.exists():
        print("Dados já existem no banco. Pulando criação...")
        return
    
    # Estados
    estados_data = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]
    
    for sigla, nome in estados_data:
        Estado.objects.get_or_create(codigo=sigla, defaults={'sigla': sigla, 'descricao': nome})
    
    print(f"Estados criados: {Estado.objects.count()}")
    
    # Algumas cidades principais
    sp = Estado.objects.get(sigla='SP')
    rj = Estado.objects.get(sigla='RJ')
    mg = Estado.objects.get(sigla='MG')
    
    cidades_data = [
        # (codigo, nome, estado, codigo_ibge)
        ('SP-SP', 'São Paulo', sp, '3550308'),
        ('RJ-RJ', 'Rio de Janeiro', rj, '3304557'),
        ('MG-BH', 'Belo Horizonte', mg, '3106200'),
        ('SP-CAM', 'Campinas', sp, '3509502'),
        ('SP-SAN', 'Santos', sp, '3548500'),
        ('RJ-NIT', 'Niterói', rj, '3303302'),
        ('MG-UBE', 'Uberlândia', mg, '3170206'),
    ]
    
    for codigo_cidade, nome, estado, codigo_ibge in cidades_data:
        Cidade.objects.get_or_create(
            codigo=codigo_cidade, # Usar o código como chave de busca principal
            estado=estado,
            defaults={'codigo_ibge': codigo_ibge}
        )
    
    print(f"Cidades criadas: {Cidade.objects.count()}")
    
    # Tipos de Pessoa
    tipos_pessoa = [
        ('1', 'Pessoa Física'),
        ('2', 'Pessoa Jurídica'),
    ]
    
    for codigo, descricao in tipos_pessoa:
        TipoPessoa.objects.get_or_create(codigo=codigo, defaults={'descricao': descricao})
    
    # Segmentos de Mercado
    segmentos = [
        ('001', 'Varejo'),
        ('002', 'Atacado'),
        ('003', 'Indústria'),
        ('004', 'Serviços'),
        ('005', 'Governo'),
    ]
    
    for codigo, descricao in segmentos:
        SegmentoMercado.objects.get_or_create(codigo=codigo, defaults={'descricao': descricao})
    
    # Formas de Pagamento
    formas_pagamento = [
        ('001', 'Dinheiro'),
        ('002', 'Cartão de Crédito'),
        ('003', 'Cartão de Débito'),
        ('004', 'PIX'),
        ('005', 'Boleto Bancário'),
        ('006', 'Transferência Bancária'),
        ('007', 'Cheque'),
    ]
    
    for codigo, descricao in formas_pagamento:
        FormaPagamento.objects.get_or_create(codigo=codigo, defaults={'descricao': descricao})
    
    # Unidades de Medida
    unidades = [
        ('UN', 'Unidade'),
        ('PC', 'Peça'),
        ('KG', 'Quilograma'),
        ('G', 'Grama'),
        ('L', 'Litro'),
        ('ML', 'Mililitro'),
        ('M', 'Metro'),
        ('CM', 'Centímetro'),
        ('M2', 'Metro Quadrado'),
        ('M3', 'Metro Cúbico'),
        ('CX', 'Caixa'),
        ('PCT', 'Pacote'),
    ]
    
    for codigo, descricao in unidades:
        # O primeiro elemento da tupla é a sigla, que também será usada como código
        sigla = codigo 
        # Apenas uma chamada get_or_create, garantindo que tanto 'codigo' quanto 'sigla' sejam definidos.
        UnidadeMedida.objects.get_or_create(codigo=codigo, defaults={'descricao': descricao, 'sigla': sigla}) 
    
    # Categorias de Produto
    categorias = [
        ('001', 'Eletrônicos'),
        ('002', 'Roupas e Acessórios'),
        ('003', 'Casa e Jardim'),
        ('004', 'Esportes e Lazer'),
        ('005', 'Livros e Mídia'),
        ('006', 'Alimentação'),
        ('007', 'Saúde e Beleza'),
        ('008', 'Automotivo'),
        ('009', 'Ferramentas'),
        ('010', 'Escritório'),
    ]
    
    for codigo, descricao in categorias:
        CategoriaProduto.objects.get_or_create(codigo=codigo, defaults={'descricao': descricao})
    
    # Tipos de Movimentação de Estoque
    tipos_movimentacao = [
        ('ENTRADA', 'Entrada', 'E'),
        ('SAIDA', 'Saída', 'S'),
        ('AJUSTE_POS', 'Ajuste Positivo', 'E'),
        ('AJUSTE_NEG', 'Ajuste Negativo', 'S'),
        ('TRANSFERENCIA', 'Transferência', 'S'),
        ('INVENTARIO', 'Inventário', 'E'),
        ('VENDA', 'Venda', 'S'),
        ('COMPRA', 'Compra', 'E'),
        ('DEVOLUCAO_VENDA', 'Devolução de Venda', 'E'),
        ('DEVOLUCAO_COMPRA', 'Devolução de Compra', 'S'),
    ]
    
    for codigo, descricao, tipo in tipos_movimentacao:
        TipoMovimentacao.objects.get_or_create(
            codigo=codigo,
            defaults={'descricao': descricao, 'tipo': tipo}
        )
    
    # Locais de Estoque
    locais_estoque = [
        ('001', 'Estoque Principal', 'Rua Principal, 123'),
        ('002', 'Estoque Filial', 'Av. Secundária, 456'),
        ('003', 'Estoque Terceirizado', 'Rua do Depósito, 789'),
    ]
    
    for codigo, descricao, endereco in locais_estoque:
        LocalEstoque.objects.get_or_create(
            codigo=codigo,
            defaults={'descricao': descricao, 'endereco': endereco}
        )
    
    # Tipos de Conta
    tipos_conta = [
        ('ATIVO', 'Ativo', 'D'),
        ('PASSIVO', 'Passivo', 'C'),
        ('PATRIMONIO', 'Patrimônio Líquido', 'C'),
        ('RECEITA', 'Receita', 'C'),
        ('DESPESA', 'Despesa', 'D'),
    ]
    
    for codigo, descricao, natureza in tipos_conta:
        TipoConta.objects.get_or_create(
            codigo=codigo,
            defaults={'descricao': descricao, 'natureza': natureza}
        )
    
    # Centros de Custo
    centros_custo = [
        ('001', 'Administração'),
        ('002', 'Vendas'),
        ('003', 'Produção'),
        ('004', 'Marketing'),
        ('005', 'Financeiro'),
    ]
    
    for codigo, descricao in centros_custo:
        CentroCusto.objects.get_or_create(
            codigo=codigo,
            defaults={'descricao': descricao}
        )
    
    print("Dados iniciais criados com sucesso!")
    print(f"- Estados: {Estado.objects.count()}")
    print(f"- Cidades: {Cidade.objects.count()}")
    print(f"- Tipos de Pessoa: {TipoPessoa.objects.count()}")
    print(f"- Segmentos de Mercado: {SegmentoMercado.objects.count()}")
    print(f"- Formas de Pagamento: {FormaPagamento.objects.count()}")
    print(f"- Unidades de Medida: {UnidadeMedida.objects.count()}")
    print(f"- Categorias de Produto: {CategoriaProduto.objects.count()}")
    print(f"- Tipos de Movimentação: {TipoMovimentacao.objects.count()}")
    print(f"- Locais de Estoque: {LocalEstoque.objects.count()}")
    print(f"- Tipos de Conta: {TipoConta.objects.count()}")
    print(f"- Centros de Custo: {CentroCusto.objects.count()}")

if __name__ == '__main__':
    criar_dados_iniciais()
