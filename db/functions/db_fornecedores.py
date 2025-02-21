# data/database.py
import sqlite3
from utils.get_globals import get_dbpath

# Caminho do banco de dados
dbpath = get_dbpath()

def conectar():
    conn = sqlite3.connect(dbpath)
    return conn

def inserir_fornecedor(nome, cnpj, contato, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fornecedores (nome, cnpj, contato, email)
        VALUES (?, ?, ?, ?)
    """, (nome, cnpj, contato, email))
    conn.commit()
    conn.close()

def obter_fornecedores():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fornecedores")
    fornecedores = cursor.fetchall()
    conn.close()
    return fornecedores

def obter_fornecedores_combobox():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM fornecedores")
    fornecedores = cursor.fetchall()
    conn.close()
    return fornecedores

def alterar_fornecedor(id, nome, cnpj, contato, email):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE fornecedores
        SET nome = ?, cnpj = ?, contato = ?, email = ?
        WHERE id = ?
    """, (nome, cnpj, contato, email, id))
    conn.commit()
    conn.close()
                
def deletar_fornecedor(id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fornecedores WHERE id = ?", (int(id),))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return e

def obter_fornecedor_por_id(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fornecedores WHERE id = ?", (id,))
    fornecedor = cursor.fetchone()  # Retorna uma tupla com os dados do fornecedor
    conn.close()
    return fornecedor
