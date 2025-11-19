# Sistema Clientes & Pedidos (SQLite)

Este repositório contém um script Python simples que implementa um pequeno sistema de gerenciamento de clientes e pedidos, conforme o plano:

1. Estrutura do Banco de Dados
   - Tabelas: `clientes` (id, nome, email, telefone) e `pedidos` (id, cliente_id [FK], produto, valor, data)

2. Funcionalidades Obrigatórias
   - Operações CRUD para ambas as tabelas
   - Consultas que relacionam pedidos aos seus clientes (JOIN)

3. Interface
   - Menu interativo via terminal para acessar todas as funcionalidades

4. Documentação
   - Comentários no código e este README explicando como usar o sistema

## Requisitos
- Python 3.8 ou superior
- Nenhuma dependência externa (usa `sqlite3` da biblioteca padrão)

## Como usar
1. Clone (ou copie) os arquivos para um diretório.
2. Execute:
```bash
python app.py
```
3. Use o menu interativo:
- 1: Listar clientes
- 2: Criar cliente
- 3: Atualizar cliente
- 4: Deletar cliente
- 5: Listar pedidos
- 6: Criar pedido
- 7: Atualizar pedido
- 8: Deletar pedido
- 9: Listar pedidos com dados do cliente (JOIN)
- 10: Popular exemplo (seed)
- 0: Sair

O banco de dados será criado localmente como `app.db` no mesmo diretório.

## Estrutura das tabelas
- clientes:
  - id (INTEGER PRIMARY KEY AUTOINCREMENT)
  - nome (TEXT)
  - email (TEXT)
  - telefone (TEXT)

- pedidos:
  - id (INTEGER PRIMARY KEY AUTOINCREMENT)
  - cliente_id (INTEGER, FK para clientes.id)
  - produto (TEXT)
  - valor (REAL)
  - data (TEXT, formato AAAA-MM-DD)

## Notas de implementação
- O script usa SQLite para simplificar a execução local sem necessidade de servidor de banco.
- Exemplo de seed inserido via opção do menu (10) — não sobrescreve dados existentes.
- Ao deletar um cliente, os pedidos associados não são automaticamente tratados no menu (o FK foi definido com ON DELETE CASCADE, mas o comportamento depende da versão do SQLite ativar foreign key enforcement; se necessário, habilite PRAGMA foreign_keys=ON).

## Melhorias possíveis
- Validação mais robusta de campos (emails, telefones).
- Interface web ou API REST.
- Export/Import CSV.
- Testes automatizados.
