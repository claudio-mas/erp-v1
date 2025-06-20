# Sistema ERP - Meu ERP

## Visão Geral

Este é um sistema ERP (Enterprise Resource Planning) completo desenvolvido em Django com suporte a SQL Server, seguindo a estrutura modular especificada:

```
Meu ERP
├── Cadastros
│   ├── Clientes
│   ├── Fornecedores
│   ├── Produtos
│   ├── Vendedores
│   └── Tabelas Auxiliares
├── Vendas
│   ├── Orçamentos
│   ├── Pedidos de Venda
│   ├── Comissionamento
│   └── Relatórios
├── Estoque
│   ├── Pedidos de Venda
│   ├── Inventário
│   └── Relatórios
└── Financeiro
    ├── Plano de Contas
    ├── Contas a Pagar
    ├── Contas a Receber
    ├── Fluxo de Caixa
    ├── DRE
    └── Relatórios
```

## Tecnologias Utilizadas

- **Backend**: Django 5.2.3
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Banco de Dados**: SQLite (desenvolvimento) / SQL Server (produção)
- **Linguagem**: Python 3.11

## Funcionalidades Implementadas

### Módulo de Cadastros
- **Clientes**: Cadastro completo com dados pessoais, endereço, contato e informações comerciais
- **Fornecedores**: Gestão de fornecedores com dados completos
- **Produtos**: Controle de produtos com preços, estoque e categorização
- **Vendedores**: Cadastro de vendedores com comissionamento
- **Tabelas Auxiliares**: Estados, cidades, tipos de pessoa, segmentos, formas de pagamento, etc.

### Módulo de Vendas
- **Orçamentos**: Criação e gestão de orçamentos
- **Pedidos de Venda**: Processamento de pedidos com itens
- **Comissionamento**: Cálculo automático de comissões
- **Relatórios**: Relatórios de vendas e performance

### Módulo de Estoque
- **Controle de Estoque**: Movimentações de entrada e saída
- **Inventário**: Gestão de inventários periódicos
- **Relatórios**: Relatórios de estoque e movimentações

### Módulo Financeiro
- **Plano de Contas**: Estrutura contábil completa
- **Contas a Pagar**: Gestão de obrigações financeiras
- **Contas a Receber**: Controle de recebimentos
- **Fluxo de Caixa**: Controle de entradas e saídas
- **DRE**: Demonstrativo de Resultado do Exercício
- **Relatórios**: Relatórios financeiros diversos

## Estrutura do Projeto

```
erp_system/
├── manage.py
├── meu_erp/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── cadastros/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── vendas/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── estoque/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── financeiro/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   └── cadastros/
└── static/
```

## Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- pip (gerenciador de pacotes Python)
- SQL Server (para produção)

### Instalação

1. **Clone ou baixe o projeto**
```bash
cd /caminho/para/o/projeto
```

2. **Instale as dependências**
```bash
pip install django djangorestframework django-cors-headers pyodbc django-mssql
```

3. **Configure o banco de dados**
   - Para desenvolvimento: SQLite (já configurado)
   - Para produção: SQL Server (veja seção de configuração)

4. **Execute as migrações**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

6. **Popule dados iniciais**
```bash
python criar_dados_iniciais.py
```

7. **Inicie o servidor**
```bash
python manage.py runserver
```

### Configuração do SQL Server

Para usar SQL Server em produção, edite o arquivo `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'meu_erp_db',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes'
        },
    }
}
```

## Acesso ao Sistema

### Django Admin
- URL: `http://localhost:8000/admin/`
- Usuário: admin
- Senha: admin123

### URLs dos Módulos
- Cadastros: `http://localhost:8000/cadastros/`
- Vendas: `http://localhost:8000/vendas/`
- Estoque: `http://localhost:8000/estoque/`
- Financeiro: `http://localhost:8000/financeiro/`

## Modelos de Dados

### Principais Entidades

#### Cadastros
- **Cliente**: Dados completos do cliente
- **Fornecedor**: Informações do fornecedor
- **Produto**: Catálogo de produtos
- **Vendedor**: Dados dos vendedores

#### Vendas
- **Orçamento**: Propostas comerciais
- **PedidoVenda**: Pedidos confirmados
- **ItemPedidoVenda**: Itens dos pedidos

#### Estoque
- **MovimentacaoEstoque**: Movimentações de estoque
- **Inventario**: Inventários periódicos
- **EstoqueProduto**: Saldo atual por produto

#### Financeiro
- **PlanoContas**: Estrutura contábil
- **ContasPagar**: Obrigações a pagar
- **ContasReceber**: Valores a receber
- **FluxoCaixa**: Movimentações financeiras

## Funcionalidades Administrativas

O sistema inclui interface administrativa completa através do Django Admin:

- Gestão de usuários e permissões
- CRUD completo para todas as entidades
- Filtros e busca avançada
- Relatórios básicos
- Auditoria de alterações

## Segurança

- Autenticação obrigatória
- Controle de permissões por usuário
- Proteção CSRF
- Validação de dados
- Logs de auditoria

## Próximos Passos

### Melhorias Sugeridas
1. **Interface Web Personalizada**: Desenvolver interface específica para cada módulo
2. **Relatórios Avançados**: Implementar relatórios com gráficos e dashboards
3. **API REST**: Criar APIs para integração com outros sistemas
4. **Notificações**: Sistema de alertas e notificações
5. **Backup Automático**: Rotinas de backup do banco de dados
6. **Auditoria Avançada**: Log detalhado de todas as operações

### Integrações Possíveis
- Sistemas de pagamento (PIX, cartões)
- E-commerce (Magento, WooCommerce)
- Contabilidade (sistemas contábeis)
- Nota Fiscal Eletrônica (NFe, NFCe)

## Suporte e Manutenção

### Logs do Sistema
Os logs do Django são salvos automaticamente e podem ser consultados para debugging.

### Backup do Banco de Dados
```bash
# SQLite
cp db.sqlite3 backup_$(date +%Y%m%d).sqlite3

# SQL Server
# Use ferramentas nativas do SQL Server
```

### Atualizações
Para atualizar o sistema:
1. Faça backup do banco de dados
2. Atualize o código
3. Execute `python manage.py migrate`
4. Reinicie o servidor

## Contato

Para suporte técnico ou dúvidas sobre o sistema, consulte a documentação do Django ou entre em contato com a equipe de desenvolvimento.

---

**Sistema ERP - Meu ERP**  
Versão 1.0  
Desenvolvido com Django Framework

