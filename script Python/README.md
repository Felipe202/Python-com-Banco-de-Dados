# 📦 Sistema de Gestão de Clientes e Pedidos

Este projeto é um script Python de console (CLI) para gerenciar o cadastro de clientes e seus respectivos pedidos. Ele utiliza um banco de dados **SQLite** (`gestao.db`) para armazenar os dados de forma persistente.

## 🚀 Funcionalidades

O sistema permite operações CRUD (Criar, Ler, Atualizar, Deletar) completas para clientes e as operações essenciais para pedidos.

### Gestão de Clientes
* **Adicionar:** Cadastra um novo cliente (nome, email, telefone).
* **Listar:** Exibe todos os clientes cadastrados.
* **Atualizar:** Permite editar as informações de um cliente existente.
* **Deletar:** Remove um cliente do banco de dados. (Atenção: Isso também removerá todos os pedidos associados a ele, graças à configuração `ON DELETE CASCADE` do banco de dados).

### Gestão de Pedidos
* **Adicionar:** Cria um novo pedido (produto, valor, data) e o vincula a um cliente existente.
* **Listar (Relacionado):** Exibe todos os pedidos, mostrando qual cliente fez qual pedido (usando `JOIN` do SQL).
* **Deletar:** Remove um pedido específico.

## 🛠️ Estrutura do Banco de Dados

O sistema cria automaticamente um arquivo `gestao.db` (SQLite) com as seguintes tabelas:

1.  **`clientes`**:
    * `id` (INTEGER, Chave Primária, Autoincremento)
    * `nome` (TEXT, Obrigatório)
    * `email` (TEXT, Obrigatório, Único)
    * `telefone` (TEXT)

2.  **`pedidos`**:
    * `id` (INTEGER, Chave Primária, Autoincremento)
    * `cliente_id` (INTEGER, Chave Estrangeira de `clientes.id`)
    * `produto` (TEXT, Obrigatório)
    * `valor` (REAL, Obrigatório)
    * `data` (TEXT, Obrigatório)

## 🐍 Como Usar

### Pré-requisitos
* **Python 3.x** instalado.

O script utiliza apenas módulos da biblioteca padrão do Python (`sqlite3`, `datetime`), portanto **não há necessidade de instalar pacotes externos** (sem `pip install`).

### Execução

1.  Salve o código principal em um arquivo chamado `gestao.py`.
2.  Abra seu terminal ou prompt de comando.
3.  Navegue até o diretório onde você salvou o arquivo.
4.  Execute o script:

```bash
python gestao.py