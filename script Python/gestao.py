# gestao.py
"""
Script para Gerenciamento de Clientes e Pedidos.
Permite operações CRUD para clientes e pedidos,
com um menu interativo de terminal.
"""

import sqlite3
import datetime


# --- 1. Configuração do Banco de Dados ---

def conectar_bd():
    """
    Conecta ao banco de dados SQLite (gestao.db).
    Ativa o suporte a chaves estrangeiras.
    """
    try:
        conn = sqlite3.connect('gestao.db')
        # Ativa a verificação de chave estrangeira
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def criar_tabelas():
    """
    Cria as tabelas 'clientes' e 'pedidos' se não existirem.
    """
    conn = conectar_bd()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        # Tabela de Clientes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT
        );
        ''')

        # Tabela de Pedidos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            produto TEXT NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE
        );
        ''')

        conn.commit()
        # print("Tabelas verificadas/criadas com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        conn.close()


# --- 2. Funcionalidades CRUD Clientes ---

def adicionar_cliente():
    """Coleta dados e insere um novo cliente no banco."""
    nome = input("Nome do cliente: ")
    email = input("Email do cliente: ")
    telefone = input("Telefone do cliente (opcional): ")

    if not nome or not email:
        print("Erro: Nome e Email são obrigatórios.")
        return

    conn = conectar_bd()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
            (nome, email, telefone)
        )
        conn.commit()
        print(f"✅ Cliente '{nome}' adicionado com sucesso (ID: {cursor.lastrowid}).")
    except sqlite3.IntegrityError:
        print(f"Erro: O email '{email}' já está cadastrado.")
    except sqlite3.Error as e:
        print(f"Erro ao adicionar cliente: {e}")
    finally:
        conn.close()


def listar_clientes():
    """Exibe todos os clientes cadastrados."""
    conn = conectar_bd()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email, telefone FROM clientes")
        clientes = cursor.fetchall()

        if not clientes:
            print("Nenhum cliente cadastrado.")
            return False

        print("\n--- Lista de Clientes ---")
        for cliente in clientes:
            print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Email: {cliente[2]} | Telefone: {cliente[3]}")
        print("--------------------------\n")
        return True
    except sqlite3.Error as e:
        print(f"Erro ao listar clientes: {e}")
        return False
    finally:
        conn.close()


def atualizar_cliente():
    """Atualiza os dados de um cliente existente pelo ID."""
    if not listar_clientes():
        return  # Não há clientes para atualizar

    try:
        id_cliente = int(input("Digite o ID do cliente que deseja atualizar: "))
    except ValueError:
        print("Erro: ID inválido.")
        return

    nome = input(f"Novo nome (atual: ...): ")
    email = input(f"Novo email (atual: ...): ")
    telefone = input(f"Novo telefone (atual: ...): ")

    if not nome or not email:
        print("Erro: Nome e Email são obrigatórios.")
        return

    conn = conectar_bd()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?",
            (nome, email, telefone, id_cliente)
        )
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Erro: Cliente com ID {id_cliente} não encontrado.")
        else:
            print(f"✅ Cliente ID {id_cliente} atualizado com sucesso.")
    except sqlite3.IntegrityError:
        print(f"Erro: O email '{email}' já está em uso por outro cliente.")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar cliente: {e}")
    finally:
        conn.close()


def deletar_cliente():
    """Deleta um cliente pelo ID (e seus pedidos associados, via ON DELETE CASCADE)."""
    if not listar_clientes():
        return

    try:
        id_cliente = int(input("Digite o ID do cliente que deseja deletar: "))
    except ValueError:
        print("Erro: ID inválido.")
        return

    confirmacao = input(f"Tem certeza que deseja deletar o cliente ID {id_cliente}? (s/n): ").lower()

    if confirmacao == 's':
        conn = conectar_bd()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
            conn.commit()
            if cursor.rowcount == 0:
                print(f"Erro: Cliente com ID {id_cliente} não encontrado.")
            else:
                print(f"✅ Cliente ID {id_cliente} (e seus pedidos) deletado com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao deletar cliente: {e}")
        finally:
            conn.close()
    else:
        print("Operação cancelada.")


# --- 3. Funcionalidades CRUD Pedidos (e Relacionamento) ---

def adicionar_pedido():
    """Coleta dados e insere um novo pedido, vinculando a um cliente."""
    print("Selecione o cliente para o pedido:")
    if not listar_clientes():
        return

    try:
        cliente_id = int(input("Digite o ID do cliente: "))
    except ValueError:
        print("Erro: ID de cliente inválido.")
        return

    produto = input("Nome do produto: ")
    try:
        valor = float(input("Valor do pedido (ex: 49.90): "))
    except ValueError:
        print("Erro: Valor inválido.")
        return

    data_hoje = datetime.date.today().isoformat()
    data = input(f"Data do pedido (padrão: {data_hoje}): ") or data_hoje

    conn = conectar_bd()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pedidos (cliente_id, produto, valor, data) VALUES (?, ?, ?, ?)",
            (cliente_id, produto, valor, data)
        )
        conn.commit()
        print(f"✅ Pedido '{produto}' adicionado com sucesso (ID: {cursor.lastrowid}).")
    except sqlite3.IntegrityError:
        # Isso acontece se o cliente_id não existir (devido ao PRAGMA foreign_keys = ON)
        print(f"Erro: Cliente com ID {cliente_id} não encontrado.")
    except sqlite3.Error as e:
        print(f"Erro ao adicionar pedido: {e}")
    finally:
        conn.close()


def listar_todos_pedidos():
    """
    Exibe todos os pedidos cadastrados,
    mostrando os dados do cliente (JOIN).
    """
    conn = conectar_bd()
    try:
        cursor = conn.cursor()

        # Consulta (Query) que relaciona as duas tabelas
        sql = """
        SELECT 
            p.id, 
            p.produto, 
            p.valor, 
            p.data, 
            c.nome, 
            c.email
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        ORDER BY p.data DESC;
        """
        cursor.execute(sql)
        pedidos = cursor.fetchall()

        if not pedidos:
            print("Nenhum pedido cadastrado.")
            return False

        print("\n--- Lista de Todos os Pedidos (com Clientes) ---")
        for p in pedidos:
            print(f"ID Pedido: {p[0]} | Produto: {p[1]} | Valor: R${p[2]:.2f} | Data: {p[3]}")
            print(f"  -> Cliente: {p[4]} (Email: {p[5]})")
            print("-" * 20)
        print("\n")
        return True
    except sqlite3.Error as e:
        print(f"Erro ao listar pedidos: {e}")
        return False
    finally:
        conn.close()


def deletar_pedido():
    """Deleta um pedido específico pelo ID."""
    if not listar_todos_pedidos():
        return

    try:
        id_pedido = int(input("Digite o ID do pedido que deseja deletar: "))
    except ValueError:
        print("Erro: ID inválido.")
        return

    conn = conectar_bd()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id = ?", (id_pedido,))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"Erro: Pedido com ID {id_pedido} não encontrado.")
        else:
            print(f"✅ Pedido ID {id_pedido} deletado com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao deletar pedido: {e}")
    finally:
        conn.close()


# --- 4. Interface de Menu ---

def menu_clientes():
    """Menu para gerenciar clientes."""
    while True:
        print("\n--- Gerenciamento de Clientes ---")
        print("1. Adicionar Cliente")
        print("2. Listar Clientes")
        print("3. Atualizar Cliente")
        print("4. Deletar Cliente")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_cliente()
        elif opcao == '2':
            listar_clientes()
        elif opcao == '3':
            atualizar_cliente()
        elif opcao == '4':
            deletar_cliente()
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")


def menu_pedidos():
    """Menu para gerenciar pedidos."""
    while True:
        print("\n--- Gerenciamento de Pedidos ---")
        print("1. Adicionar Pedido")
        print("2. Listar Todos os Pedidos (com Clientes)")
        print("3. Deletar Pedido")
        # Nota: A atualização de pedidos foi omitida por brevidade,
        # mas seguiria o mesmo padrão de 'atualizar_cliente'.
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_pedido()
        elif opcao == '2':
            listar_todos_pedidos()
        elif opcao == '3':
            deletar_pedido()
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")


def main():
    """Função principal que executa o menu."""
    criar_tabelas()  # Garante que as tabelas existam

    while True:
        print("\n--- Sistema de Gestão de Clientes e Pedidos ---")
        print("1. Gerenciar Clientes")
        print("2. Gerenciar Pedidos")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_clientes()
        elif opcao == '2':
            menu_pedidos()
        elif opcao == '0':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    main()