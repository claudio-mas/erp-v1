# Generated by Django 5.0.14 on 2025-06-20 04:25

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10, unique=True, verbose_name='Código')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('sigla', models.CharField(max_length=2, unique=True, verbose_name='Sigla')),
            ],
            options={
                'verbose_name': 'Estado',
                'verbose_name_plural': 'Estados',
            },
        ),
        migrations.CreateModel(
            name='FormaPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10, unique=True, verbose_name='Código')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('prazo_dias', models.IntegerField(default=0, verbose_name='Prazo em Dias')),
            ],
            options={
                'verbose_name': 'Forma de Pagamento',
                'verbose_name_plural': 'Formas de Pagamento',
            },
        ),
        migrations.CreateModel(
            name='SegmentoMercado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10, unique=True, verbose_name='Código')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
            ],
            options={
                'verbose_name': 'Segmento de Mercado',
                'verbose_name_plural': 'Segmentos de Mercado',
            },
        ),
        migrations.CreateModel(
            name='TipoPessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10, unique=True, verbose_name='Código')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
            ],
            options={
                'verbose_name': 'Tipo de Pessoa',
                'verbose_name_plural': 'Tipos de Pessoa',
            },
        ),
        migrations.CreateModel(
            name='UnidadeMedida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10, unique=True, verbose_name='Código')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('sigla', models.CharField(max_length=5, unique=True, verbose_name='Sigla')),
            ],
            options={
                'verbose_name': 'Unidade de Medida',
                'verbose_name_plural': 'Unidades de Medida',
            },
        ),
        migrations.CreateModel(
            name='CategoriaProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10, unique=True, verbose_name='Código')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('categoria_pai', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.categoriaproduto', verbose_name='Categoria Pai')),
            ],
            options={
                'verbose_name': 'Categoria de Produto',
                'verbose_name_plural': 'Categorias de Produto',
            },
        ),
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10, unique=True, verbose_name='Código')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('codigo_ibge', models.CharField(blank=True, max_length=10, null=True, verbose_name='Código IBGE')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.estado', verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Cidade',
                'verbose_name_plural': 'Cidades',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, unique=True, verbose_name='Código')),
                ('nome_razao_social', models.CharField(max_length=200, verbose_name='Nome/Razão Social')),
                ('nome_fantasia', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nome Fantasia')),
                ('cpf_cnpj', models.CharField(max_length=18, unique=True, validators=[django.core.validators.RegexValidator(message='CPF deve estar no formato XXX.XXX.XXX-XX ou CNPJ no formato XX.XXX.XXX/XXXX-XX', regex='^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$|^\\d{2}\\.\\d{3}\\.\\d{3}/\\d{4}-\\d{2}$')], verbose_name='CPF/CNPJ')),
                ('rg_ie', models.CharField(blank=True, max_length=20, null=True, verbose_name='RG/IE')),
                ('endereco', models.CharField(max_length=200, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=100, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                ('cep', models.CharField(max_length=10, verbose_name='CEP')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=20, null=True, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('site', models.URLField(blank=True, null=True, verbose_name='Site')),
                ('prazo_entrega_dias', models.IntegerField(default=0, verbose_name='Prazo de Entrega (dias)')),
                ('banco', models.CharField(blank=True, max_length=100, null=True, verbose_name='Banco')),
                ('agencia', models.CharField(blank=True, max_length=20, null=True, verbose_name='Agência')),
                ('conta', models.CharField(blank=True, max_length=20, null=True, verbose_name='Conta')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.cidade', verbose_name='Cidade')),
                ('forma_pagamento_padrao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.formapagamento', verbose_name='Forma de Pagamento Padrão')),
                ('usuario_cadastro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário de Cadastro')),
                ('tipo_pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.tipopessoa', verbose_name='Tipo de Pessoa')),
            ],
            options={
                'verbose_name': 'Fornecedor',
                'verbose_name_plural': 'Fornecedores',
                'ordering': ['nome_razao_social'],
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, unique=True, verbose_name='Código')),
                ('nome_razao_social', models.CharField(max_length=200, verbose_name='Nome/Razão Social')),
                ('nome_fantasia', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nome Fantasia')),
                ('cpf_cnpj', models.CharField(max_length=18, unique=True, validators=[django.core.validators.RegexValidator(message='CPF deve estar no formato XXX.XXX.XXX-XX ou CNPJ no formato XX.XXX.XXX/XXXX-XX', regex='^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$|^\\d{2}\\.\\d{3}\\.\\d{3}/\\d{4}-\\d{2}$')], verbose_name='CPF/CNPJ')),
                ('rg_ie', models.CharField(blank=True, max_length=20, null=True, verbose_name='RG/IE')),
                ('endereco', models.CharField(max_length=200, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=100, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                ('cep', models.CharField(max_length=10, verbose_name='CEP')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=20, null=True, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('site', models.URLField(blank=True, null=True, verbose_name='Site')),
                ('limite_credito', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Limite de Crédito')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.cidade', verbose_name='Cidade')),
                ('usuario_cadastro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário de Cadastro')),
                ('forma_pagamento_padrao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.formapagamento', verbose_name='Forma de Pagamento Padrão')),
                ('segmento_mercado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.segmentomercado', verbose_name='Segmento de Mercado')),
                ('tipo_pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.tipopessoa', verbose_name='Tipo de Pessoa')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['nome_razao_social'],
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, unique=True, verbose_name='Código')),
                ('codigo_barras', models.CharField(blank=True, max_length=20, null=True, verbose_name='Código de Barras')),
                ('descricao', models.CharField(max_length=200, verbose_name='Descrição')),
                ('descricao_detalhada', models.TextField(blank=True, null=True, verbose_name='Descrição Detalhada')),
                ('preco_custo', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Preço de Custo')),
                ('preco_venda', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Preço de Venda')),
                ('margem_lucro', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Margem de Lucro (%)')),
                ('estoque_minimo', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Estoque Mínimo')),
                ('estoque_maximo', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Estoque Máximo')),
                ('estoque_atual', models.DecimalField(decimal_places=3, default=0, max_digits=15, verbose_name='Estoque Atual')),
                ('peso', models.DecimalField(decimal_places=3, default=0, max_digits=10, verbose_name='Peso (kg)')),
                ('altura', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Altura (cm)')),
                ('largura', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Largura (cm)')),
                ('profundidade', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Profundidade (cm)')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.categoriaproduto', verbose_name='Categoria')),
                ('fornecedor_padrao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.fornecedor', verbose_name='Fornecedor Padrão')),
                ('usuario_cadastro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário de Cadastro')),
                ('unidade_medida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.unidademedida', verbose_name='Unidade de Medida')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ['descricao'],
            },
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, unique=True, verbose_name='Código')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('cpf', models.CharField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message='CPF deve estar no formato XXX.XXX.XXX-XX', regex='^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$')], verbose_name='CPF')),
                ('rg', models.CharField(max_length=20, verbose_name='RG')),
                ('endereco', models.CharField(max_length=200, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=100, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                ('cep', models.CharField(max_length=10, verbose_name='CEP')),
                ('telefone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Telefone')),
                ('celular', models.CharField(max_length=20, verbose_name='Celular')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('data_admissao', models.DateField(verbose_name='Data de Admissão')),
                ('data_demissao', models.DateField(blank=True, null=True, verbose_name='Data de Demissão')),
                ('salario_base', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Salário Base')),
                ('comissao_percentual', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Comissão (%)')),
                ('meta_mensal', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Meta Mensal')),
                ('banco', models.CharField(blank=True, max_length=100, null=True, verbose_name='Banco')),
                ('agencia', models.CharField(blank=True, max_length=20, null=True, verbose_name='Agência')),
                ('conta', models.CharField(blank=True, max_length=20, null=True, verbose_name='Conta')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.cidade', verbose_name='Cidade')),
                ('usuario_cadastro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário de Cadastro')),
            ],
            options={
                'verbose_name': 'Vendedor',
                'verbose_name_plural': 'Vendedores',
                'ordering': ['nome'],
            },
        ),
    ]
