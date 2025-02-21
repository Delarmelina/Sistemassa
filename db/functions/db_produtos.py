# data/database.py
import sqlite3
from utils.get_globals import get_dbpath, get_restaurante

# Caminho do banco de dados
dbpath = get_dbpath()

def conectar():
    conn = sqlite3.connect(dbpath)
    return conn

def inserir_produto(nome, categoria_id, subcategoria_id, unidade_id, estoque_atual, descricao, quant = 0, receita = []):
    try:
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO produtos (nome, categoria_id, subcategoria_id, unidade_id, estoque_atual, descricao, quant, restaurante_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nome, categoria_id, subcategoria_id, unidade_id, estoque_atual, descricao, quant, get_restaurante()))

        last_produto_id = cursor.lastrowid

        if float(quant) > 0.0:
            for i in range(len(receita['ID Produto'])):
                cursor.execute("""
                    INSERT INTO receitas (produto_id, ingrediente_id, quantidade)
                    VALUES (?, ?, ?)
                """, (last_produto_id, receita['ID Produto'][i], receita['Quantidade'][i]))
        conn.commit()
        conn.close()
        return True  # Indica que a inserção foi bem-sucedida
    except Exception as e:
        return (f"Erro ao inserir produto: {e}")

def obter_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            p.id,
            p.nome,
            c.nome AS categoria_nome,
            s.nome AS subcategoria_nome,
            p.estoque_atual,
            u.nome AS unidade_nome,
            p.descricao,
            p.quant
        FROM produtos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        LEFT JOIN subcategorias s ON p.subcategoria_id = s.id
        LEFT JOIN unidades u ON p.unidade_id = u.id
        WHERE p.restaurante_id = ?
    """, (int(get_restaurante()),))
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def atualizar_produto(produto_id, nome, categoria_id, subcategoria_id, unidade_id, descricao, quant = 0, receita = []):
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Atualiza as informações do produto na tabela 'produtos'
        cursor.execute('''
            UPDATE produtos
            SET nome = ?, categoria_id = ?, subcategoria_id = ?, unidade_id = ?, descricao = ?, quant = ?
            WHERE id = ?
        ''', (nome, categoria_id, subcategoria_id, unidade_id, descricao, quant, produto_id))
        
        # Verifica se alguma linha foi afetada
        if cursor.rowcount == 0:
            raise Exception(f"Produto com ID {produto_id} não encontrado.")
        

        # Remover os itens antigos da receita para reescrevê-los
        cursor.execute('DELETE FROM receitas WHERE produto_id = ?', (produto_id,))

        # Inserir os novos itens
        if (float(quant) > 0.0):
            for i in receita:
                cursor.execute("""
                    INSERT INTO receitas (produto_id, ingrediente_id, quantidade)
                    VALUES (?, ?, ?)
                """, (produto_id, i[0], i[2]))
        
        conn.commit()
        conn.close()
        return "Produto atualizado com sucesso!"
    except Exception as e:
        return f"Erro ao atualizar o produto: {e}"

def obter_produto_por_id(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, p.nome, c.nome AS categoria_nome, s.nome AS subcategoria_nome, u.nome AS unidade_nome, p.estoque_atual, p.descricao, p.quant
        FROM produtos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        LEFT JOIN subcategorias s ON p.subcategoria_id = s.id
        LEFT JOIN unidades u ON p.unidade_id = u.id
        WHERE p.id = ? AND p.restaurante_id = ?
    ''', (produto_id, get_restaurante()))
    produto = cursor.fetchone()
    conn.close()
    return produto

def obter_receita_por_id(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM receitas WHERE produto_id = ?
    ''', (produto_id,))
    produto = cursor.fetchall()
    conn.close()
    return produto

def obter_produto_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, p.nome, c.nome AS categoria_nome, s.nome AS subcategoria_nome, u.nome AS unidade_nome, p.estoque_atual, p.descricao
        FROM produtos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        LEFT JOIN subcategorias s ON p.subcategoria_id = s.id
        LEFT JOIN unidades u ON p.unidade_id = u.id
        WHERE p.nome = ?
    ''', (nome,))
    produto = cursor.fetchone()
    conn.close()
    return produto

def deletar_produto(produto_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        # Deletar os itens da receita
        cursor.execute("DELETE FROM receitas WHERE produto_id = ?", (int(produto_id),))
        cursor.execute("DELETE FROM produtos WHERE id = ?", (int(produto_id),))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return f"Erro ao atualizar o produto: {e}"