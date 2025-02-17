# data/database.py
import sqlite3
from utils.get_globals import get_dbpath

# Caminho do banco de dados
dbpath = get_dbpath()

def conectar():
    conn = sqlite3.connect(dbpath)
    return conn

def excluir_categoria(categoria_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categorias WHERE id=?", (categoria_id,))
    conn.commit()
    conn.close()

def excluir_subcategoria(subcategoria_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subcategorias WHERE id=?", (subcategoria_id,))
    conn.commit()
    conn.close()

def excluir_unidade(unidade_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM unidades WHERE id=?", (unidade_id,))
    conn.commit()
    conn.close()

# Funções para Obter Categorias
def obter_categorias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM categorias")
    categorias = cursor.fetchall()
    conn.close()
    return categorias

# Funções para Obter Subcategorias
def obter_subcategorias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id as Id, s.nome as Nome, c.nome as Categoria 
        FROM subcategorias s
        JOIN categorias c ON s.categoria_id = c.id
    """)
    subcategorias = cursor.fetchall()
    conn.close()
    return subcategorias

# Funções para Obter Unidades de Medida
def obter_unidades():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM unidades")
    unidades = cursor.fetchall()
    conn.close()
    return unidades

# Funções para Inserir Categorias
def inserir_categoria(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

# Funções para Inserir Subcategorias
def inserir_subcategoria(nome, categoria_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subcategorias (nome, categoria_id) VALUES (?, ?)", (nome, categoria_id))
    conn.commit()
    conn.close()

# Funções para Inserir Unidades de Medida
def inserir_unidade(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO unidades (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def obter_subcategorias_por_categoria(categoria_nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, s.nome 
        FROM subcategorias s
        JOIN categorias c ON s.categoria_id = c.id
        WHERE c.id = ?
    """, (categoria_nome,))
    subcategorias = cursor.fetchall()
    conn.close()
    return subcategorias
