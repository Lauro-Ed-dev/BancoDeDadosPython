#!/usr/bin/env python3
"""
app.py

Sistema simples de gestão de clientes e pedidos usando SQLite.
Funcionalidades:
- Cria o banco de dados e as tabelas (clientes, pedidos)
- CRUD para clientes
- CRUD para pedidos (cada pedido referencia um cliente via cliente_id)
- Consulta que relaciona pedidos aos seus clientes
- Menu interativo via terminal

Requisitos:
- Python 3.8+
- não requer dependências externas (usa sqlite3 da stdlib)

Uso:
$ python app.py
"""

import sqlite3
import datetime
import sys
from typing import Optional, List, Tuple

DB_PATH = "app.db"

# ---------- Banco de Dados / Inicialização ----------

def get_conn():
    """Retorna uma conexão com o banco SQLite."""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Cria as tabelas clientes e pedidos se não existirem."""
    conn = get_conn()
    cur = conn.cursor()

    # Tabela de clientes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT,
        telefone TEXT
    )
    """)

    # Tabela de pedidos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        produto TEXT NOT NULL,
        valor REAL NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

# ---------- CRUD Clientes ----------

def add_client(nome: str, email: Optional[str], telefone: Optional[str]) -> int:
    """Adiciona um cliente e retorna o id criado."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                (nome, email, telefone))
    conn.commit()
    client_id = cur.lastrowid
    conn.close()
    return client_id

def get_clients() -> List[Tuple]:
    """Retorna lista de todos os clientes como tuplas (id, nome, email, telefone)."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email, telefone FROM clientes ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_client_by_id(client_id: int) -> Optional[Tuple]:
    """Retorna um cliente por id ou None se não existir."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email, telefone FROM clientes WHERE id = ?", (client_id,))
    row = cur.fetchone()
    conn.close()
    return row

def update_client(client_id: int, nome: str, email: Optional[str], telefone: Optional[str]) -> bool:
    """Atualiza dados do cliente. Retorna True se atualizou algum registro."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?",
                (nome, email, telefone, client_id))
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed

def delete_client(client_id: int) -> bool:
    """Deleta cliente por id. Retorna True se deletou algum registro."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM clientes WHERE id = ?", (client_id,))
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed

# ---------- CRUD Pedidos ----------

def add_order(cliente_id: int, produto: str, valor: float, data: str) -> int:
    """Adiciona um pedido e retorna o id criado."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO pedidos (cliente_id, produto, valor, data) VALUES (?, ?, ?, ?)",
                (cliente_id, produto, valor, data))
    conn.commit()
    order_id = cur.lastrowid
    conn.close()
    return order_id

def get_orders() -> List[Tuple]:
    """Retorna lista de todos os pedidos como (id, cliente_id, produto, valor, data)."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, cliente_id, produto, valor, data FROM pedidos ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_order_by_id(order_id: int) -> Optional[Tuple]:
    """Retorna um pedido por id ou None se não existir."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, cliente_id, produto, valor, data FROM pedidos WHERE id = ?", (order_id,))
    row = cur.fetchone()
    conn.close()
    return row

def update_order(order_id: int, cliente_id: int, produto: str, valor: float, data: str) -> bool:
    """Atualiza um pedido. Retorna True se atualizou."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    UPDATE pedidos SET cliente_id = ?, produto = ?, valor = ?, data = ?
    WHERE id = ?
    """, (cliente_id, produto, valor, data, order_id))
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed

def delete_order(order_id: int) -> bool:
    """Deleta um pedido por id. Retorna True se deletou."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM pedidos WHERE id = ?", (order_id,))
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed

# ---------- Consultas Relacionadas ----------

def list_orders_with_clients() -> List[Tuple]:
    """
    Retorna lista de pedidos com dados do cliente:
    (pedido_id, produto, valor, data, cliente_id, cliente_nome, cliente_email, cliente_telefone)
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT p.id, p.produto, p.valor, p.data, c.id, c.nome, c.email, c.telefone
    FROM pedidos p
    JOIN clientes c ON p.cliente_id = c.id
    ORDER BY p.id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

# ---------- Utilitários de Entrada ----------

def input_int(prompt: str) -> int:
    """Leitura segura de int."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

def input_float(prompt: str) -> float:
    """Leitura segura de float."""
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Entrada inválida. Digite um número (ex: 12.50).")

def input_date(prompt: str) -> str:
    """
    Lê uma data no formato AAAA-MM-DD. Se vazio, usa data atual.
    Não faz validações complexas além do parse básico.
    """
    while True:
        s = input(prompt).strip()
        if s == "":
            return datetime.date.today().isoformat()
        try:
            datetime.date.fromisoformat(s)
            return s
        except ValueError:
            print("Formato inválido. Use AAAA-MM-DD ou deixe em branco para usar a data de hoje.")

# ---------- Menu Interativo ----------

def print_header():
    print("=" * 50)
    print("Sistema Clientes & Pedidos (SQLite)".center(50))
    print("=" * 50)

def menu():
    print_header()
    print("1. Clientes: listar")
    print("2. Clientes: criar")
    print("3. Clientes: atualizar")
    print("4. Clientes: deletar")
    print("5. Pedidos: listar")
    print("6. Pedidos: criar")
    print("7. Pedidos: atualizar")
    print("8. Pedidos: deletar")
    print("9. Listar pedidos com dados do cliente (JOIN)")
    print("10. Popular exemplo (seed)")
    print("0. Sair")
    print("-" * 50)

def seed_example():
    """Insere alguns dados de exemplo no banco."""
    # Inserir apenas se tabela vazia
    if get_clients():
        print("O banco já possui dados. Seed não será aplicado.")
        return
    c1 = add_client("Ana Silva", "ana@example.com", "11999990000")
    c2 = add_client("Bruno Costa", "bruno@example.com", "21988880000")
    add_order(c1, "Teclado mecânico", 299.90, datetime.date.today().isoformat())
    add_order(c2, "Monitor 24\"", 799.50, datetime.date.today().isoformat())
    print("Dados de exemplo inseridos.")

def main_loop():
    init_db()
    while True:
        menu()
        choice = input("Escolha uma opção: ").strip()
        if choice == "1":
            clients = get_clients()
            if not clients:
                print("Nenhum cliente cadastrado.")
            else:
                print("Clientes:")
                for c in clients:
                    print(f"ID={c[0]} | Nome={c[1]} | Email={c[2]} | Telefone={c[3]}")
        elif choice == "2":
            nome = input("Nome: ").strip()
            email = input("Email (opcional): ").strip() or None
            telefone = input("Telefone (opcional): ").strip() or None
            if not nome:
                print("Nome é obrigatório.")
                continue
            cid = add_client(nome, email, telefone)
            print(f"Cliente criado com id {cid}.")
        elif choice == "3":
            client_id = input_int("ID do cliente a atualizar: ")
            existing = get_client_by_id(client_id)
            if not existing:
                print("Cliente não encontrado.")
                continue
            print(f"Atualizando cliente (atual) Nome={existing[1]}, Email={existing[2]}, Telefone={existing[3]}")
            nome = input("Novo nome (deixe em branco para manter): ").strip() or existing[1]
            email = input("Novo email (deixe em branco para manter): ").strip() or existing[2]
            telefone = input("Novo telefone (deixe em branco para manter): ").strip() or existing[3]
            success = update_client(client_id, nome, email, telefone)
            print("Atualizado." if success else "Falha ao atualizar.")
        elif choice == "4":
            client_id = input_int("ID do cliente a deletar: ")
            success = delete_client(client_id)
            print("Cliente deletado." if success else "Cliente não encontrado.")
        elif choice == "5":
            orders = get_orders()
            if not orders:
                print("Nenhum pedido cadastrado.")
            else:
                print("Pedidos:")
                for o in orders:
                    print(f"ID={o[0]} | ClienteID={o[1]} | Produto={o[2]} | Valor={o[3]} | Data={o[4]}")
        elif choice == "6":
            cliente_id = input_int("ID do cliente para este pedido: ")
            if not get_client_by_id(cliente_id):
                print("Cliente não existe. Crie o cliente primeiro.")
                continue
            produto = input("Produto: ").strip()
            valor = input_float("Valor (ex: 199.90): ")
            data = input_date("Data (AAAA-MM-DD, deixe em branco para hoje): ")
            oid = add_order(cliente_id, produto, valor, data)
            print(f"Pedido criado com id {oid}.")
        elif choice == "7":
            order_id = input_int("ID do pedido a atualizar: ")
            existing = get_order_by_id(order_id)
            if not existing:
                print("Pedido não encontrado.")
                continue
            print(f"Atualizando pedido (atual) ClienteID={existing[1]}, Produto={existing[2]}, Valor={existing[3]}, Data={existing[4]}")
            cliente_id = input_int("Novo Cliente ID (ou o mesmo): ")
            if not get_client_by_id(cliente_id):
                print("Cliente não existe.")
                continue
            produto = input("Novo produto (deixe em branco para manter): ").strip() or existing[2]
            valor_input = input("Novo valor (deixe em branco para manter): ").strip()
            valor = float(valor_input) if valor_input else existing[3]
            data = input("Nova data AAAA-MM-DD (deixe em branco para manter): ").strip() or existing[4]
            success = update_order(order_id, cliente_id, produto, valor, data)
            print("Pedido atualizado." if success else "Falha ao atualizar.")
        elif choice == "8":
            order_id = input_int("ID do pedido a deletar: ")
            success = delete_order(order_id)
            print("Pedido deletado." if success else "Pedido não encontrado.")
        elif choice == "9":
            rows = list_orders_with_clients()
            if not rows:
                print("Nenhum pedido com cliente encontrado.")
            else:
                for r in rows:
                    print(f"PedidoID={r[0]} | Produto={r[1]} | Valor={r[2]} | Data={r[3]}")
                    print(f"  -> ClienteID={r[4]} | Nome={r[5]} | Email={r[6]} | Telefone={r[7]}")
                    print("-" * 40)
        elif choice == "10":
            seed_example()
        elif choice == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário. Até mais!")
        sys.exit(0)