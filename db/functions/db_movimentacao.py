# data/database.py
import sqlite3
from utils.get_globals import get_dbpath, get_restaurante

# Caminho do banco de dados
dbpath = get_dbpath()

def conectar():
    conn = sqlite3.connect(dbpath)
    return conn

# -----------------------------------
# ENTRADAS
# -----------------------------------

def inserir_entrada(data, tipo, observacao, dados = []):
    
    id_restaurante = int(get_restaurante())

    try:
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO movimetacoes (id_restaurante, data, tipo, origem_id, observacao)
            VALUES (?, ?, ?, NULL, ?)
        """, (id_restaurante, data, tipo, observacao))

        last_produto_id = cursor.lastrowid

        if len(dados) > 0:
            for i in range(len(dados['ID Produto'])):
                cursor.execute("""
                    INSERT INTO movimentacoes_itens (movimentacao_id, produto_id, quantidade, tipo_movimentacao)
                    VALUES (?, ?, ?, entrada)
                """, (last_produto_id, dados['ID Produto'][i], dados['Quantidade'][i]))
        conn.commit()
        conn.close()
        return True  # Indica que a inserção foi bem-sucedida
    except Exception as e:
        return (f"Erro ao inserir produto: {e}")
    
def obter_movimentacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT m.id as ID, m.tipo as Tipo, m.data as Data, r.nome as Restaurante, o.nome as Origem, m.fornecedor as Fornecedor, m.observacao as Observações
        FROM movimentacoes m
        LEFT JOIN restaurantes r ON r.id = m.id_restaurante
		LEFT JOIN restaurantes o ON o.id = m.origem_id
        LEFT JOIN fornecedores f ON f.id = m.fornecedor_id
		WHERE r.id = 1 or o.id = 1
        """)
    movimentacoes = cursor.fetchall()
    conn.close()
    return movimentacoes