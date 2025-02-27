#database_structure.py
import sqlite3
from utils.get_globals import get_dbpath

# Caminho do banco de dados
dbpath = get_dbpath()
print(dbpath)

def conectar():
    """Função para conectar ao banco de dados"""
    conn = sqlite3.connect(dbpath)
    return conn

def criar_banco():  
    # Conectar ao banco de dados (ele será criado se não existir)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    print(dbpath)

    criar_tabela_usuarios = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    );
    """

    criar_relacao_user_restaurante = """
    CREATE TABLE IF NOT EXISTS user_restaurante (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        restaurante_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES usuarios(id),
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)
    );
    """

    criar_restaurantes = """
        CREATE TABLE IF NOT EXISTS restaurantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        );
    """
    
    # SQL para criar as tabelas
    criar_produtos = """
        CREATE TABLE IF NOT EXISTS produtos (
        "id"	INTEGER,
        "nome"	TEXT NOT NULL,
        "categoria_id"	INTEGER NOT NULL,
        "subcategoria_id"	INTEGER,
        "unidade_id"	INTEGER NOT NULL,
        "estoque_atual"	REAL NOT NULL DEFAULT 0,
        "descricao"	TEXT,
        "quant" REAL DEFAULT 0,
        "restaurante_id" INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id),
        FOREIGN KEY("subcategoria_id") REFERENCES "subcategorias"("id"),
        FOREIGN KEY("unidade_id") REFERENCES "unidades",
        FOREIGN KEY("categoria_id") REFERENCES "categorias"("id")
    );
    """
    
    criar_fornecedores = """
    CREATE TABLE IF NOT EXISTS fornecedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cnpj TEXT NOT NULL UNIQUE,
        contato TEXT,
        email TEXT
    );
    """
    
    criar_detalhes_receitas = """
    CREATE TABLE IF NOT EXISTS receitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        ingrediente_id INTEGER NOT NULL,
        quantidade REAL,
        FOREIGN KEY (produto_id) REFERENCES produtos(id),
        FOREIGN KEY (ingrediente_id) REFERENCES produtos(id)
    );
    """

    # Tabela de Categorias
    criar_categorias = """
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );
    """
    
    # Tabela de Subcategorias
    criar_subcategorias = """
    CREATE TABLE IF NOT EXISTS subcategorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY(categoria_id) REFERENCES categorias(id)
    );
    """
    
    # Tabela de Unidades de Medida
    criar_unidades = """
    CREATE TABLE IF NOT EXISTS unidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );
    """

    # Tabela de Movimentações
    criar_movimentacoes = """
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_restaurante INTEGER NOT NULL,
        data DATETIME NOT NULL,
        tipo TEXT CHECK(tipo IN ('entrada', 'saida', 'producao', 'transferencia')) NOT NULL,
        origem_id INTEGER,
        observacao TEXT,
        FOREIGN KEY (id_restaurante) REFERENCES restaurantes(id),
        FOREIGN KEY (origem_id) REFERENCES restaurantes(id)
    );
    """

    criar_movimentacoes_itens = """
    CREATE TABLE IF NOT EXISTS movimentacoes_itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movimentacao_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade REAL NOT NULL,
        tipo_movimentacao TEXT CHECK(tipo_movimentacao IN('entrada', 'saida')) NOT NULL,
        FOREIGN KEY(movimentacao_id) REFERENCES movimentacoes(id),
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    );
    """

    # Executando os comandos SQL para criar as tabelas
    cursor.execute(criar_tabela_usuarios)
    cursor.execute(criar_relacao_user_restaurante)
    
    cursor.execute(criar_restaurantes)
    cursor.execute(criar_produtos)
    cursor.execute(criar_fornecedores)
    cursor.execute(criar_detalhes_receitas)

    cursor.execute(criar_movimentacoes)
    cursor.execute(criar_movimentacoes_itens)

    cursor.execute(criar_unidades)
    cursor.execute(criar_subcategorias)
    cursor.execute(criar_categorias)

    # #Trigger que sempre que uma produção for inserida, o estoque do produto produzido é atualizado e o estoque dos ingredientes é decrementado
    # criar_trriger_insert_producao = """
    # CREATE TRIGGER IF NOT EXISTS atualizar_estoque_after_insert_producao
    # AFTER INSERT ON producoes
    # FOR EACH ROW
    # BEGIN
    #     -- Registrar a saída com o motivo de produção
    #     INSERT INTO saidas (data, motivo_id, restaurante_id, observacoes)
    #     VALUES (NEW.data, (SELECT id FROM motivos_saidas WHERE nome = 'Produção'), NEW.restaurante_id, 'Saída de ingredientes para produção');

    #     -- Recuperar o ID da saída recém-criada
    #     INSERT INTO itens_saidas (saida_id, produto_id, quantidade)
    #     SELECT last_insert_rowid(), ingrediente_id, quantidade * NEW.quantidade
    #     FROM receitas
    #     WHERE produto_id = NEW.produto_id;

    #     -- Atualizar o estoque do produto produzido
    #     UPDATE produtos
    #     SET estoque_atual = estoque_atual + NEW.quantidade
    #     WHERE id = NEW.produto_id 
    #     AND restaurante_id = NEW.restaurante_id;
    # END;
    # """

    # criar_trigger_insert_entrada = """
    # CREATE TRIGGER IF NOT EXISTS atualizar_estoque_after_insert_entradas
    # AFTER INSERT ON itens_entradas
    # FOR EACH ROW
    # BEGIN
    #     UPDATE produtos
    #     SET estoque_atual = estoque_atual + NEW.quantidade
    #     WHERE id = NEW.produto_id;
    # END;
    # """
    
    # # Criar o trigger para atualizar o estoque após uma alteração
    # criar_trigger_update_entrada = """
    # CREATE TRIGGER IF NOT EXISTS atualizar_estoque_after_update_entradas
    # AFTER UPDATE ON itens_entradas
    # FOR EACH ROW
    # BEGIN
    #     -- Primeiro, remove a quantidade anterior
    #     UPDATE produtos
    #     SET estoque_atual = estoque_atual - OLD.quantidade
    #     WHERE id = OLD.produto_id
    #     AND restaurante_id = (SELECT restaurante_id FROM entradas WHERE id = NEW.entrada_id);

    #     -- Depois, adiciona a nova quantidade
    #     UPDATE produtos
    #     SET estoque_atual = estoque_atual + NEW.quantidade
    #     WHERE id = NEW.produto_id
    #     AND restaurante_id = (SELECT restaurante_id FROM entradas WHERE id = NEW.entrada_id);
    # END;
    # """
    
    # # Criar o trigger para atualizar o estoque após a exclusão
    # criar_trigger_delete_entrada = """
    # CREATE TRIGGER IF NOT EXISTS atualizar_estoque_after_delete_entradas
    # AFTER DELETE ON itens_entradas
    # FOR EACH ROW
    # BEGIN
    #     UPDATE produtos
    #     SET estoque_atual = estoque_atual - OLD.quantidade
    #     WHERE id = OLD.produto_id;
    # END;
    # """

    # criar_trigger_insert_saida = """
    # CREATE TRIGGER IF NOT EXISTS atualizar_estoque_after_insert_saidas
    # AFTER INSERT ON itens_saidas
    # FOR EACH ROW
    # BEGIN
    #     UPDATE produtos
    #     SET estoque_atual = estoque_atual - NEW.quantidade
    #     WHERE id = NEW.produto_id 
    #     AND restaurante_id = (SELECT restaurante_id FROM saidas WHERE id = NEW.saida_id);
    # END;
    # """
    
    # # Criar o trigger para atualizar o estoque após uma alteração
    # criar_trigger_update_saida = """
    # CREATE TRIGGER IF NOT EXISTS atualizar_estoque_after_update_saidas
    # AFTER UPDATE ON itens_saidas
    # FOR EACH ROW
    # BEGIN
    #     -- Primeiro, remove a quantidade anterior
    #     UPDATE produtos
    #     SET estoque_atual = estoque_atual + OLD.quantidade
    #     WHERE id = OLD.produto_id
    #     AND restaurante_id = (SELECT restaurante_id FROM saidas WHERE id = NEW.saida_id);

    #     -- Depois, adiciona a nova quantidade
    #     UPDATE produtos
    #     SET estoque_atual = estoque_atual - NEW.quantidade
    #     WHERE id = NEW.produto_id
    #     AND restaurante_id = (SELECT restaurante_id FROM saidas WHERE id = NEW.saida_id);
    # END;
    # """
    
    # # Criar o trigger para atualizar o estoque após a exclusão
    # criar_trigger_delete_saida = """
    # CREATE TRIGGER IF NOT EXISTS atualizar_estoque_after_delete_saidas
    # AFTER DELETE ON itens_saidas
    # FOR EACH ROW
    # BEGIN
    #     UPDATE produtos
    #     SET estoque_atual = estoque_atual + OLD.quantidade
    #     WHERE id = OLD.produto_id
    #     AND restaurante_id = (SELECT restaurante_id FROM saidas WHERE id = NEW.saida_id);
    # END;
    # """
    
    # # Executar os triggers
    # cursor.execute(criar_trriger_insert_producao)
    # cursor.execute(criar_trigger_insert_entrada)
    # cursor.execute(criar_trigger_update_entrada)
    # cursor.execute(criar_trigger_delete_entrada)
    # cursor.execute(criar_trigger_insert_saida)
    # cursor.execute(criar_trigger_update_saida)
    # cursor.execute(criar_trigger_delete_saida)
    
    # Comitar e fechar a conexão
    conn.commit()
    conn.close()
    print("Banco de dados e tabelas atualizados com sucesso!")
    