# data/database.py
import sqlite3
from utils.get_globals import get_dbpath, get_usuario_id

# Caminho do banco de dados
dbpath = get_dbpath()

def conectar():
    conn = sqlite3.connect(dbpath)
    return conn

def excluir_restaurante(restaurante_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM restaurantes WHERE id=?", (int(restaurante_id),))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return e

# Funções para Obter restaurantes de Medida
def obter_restaurantes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM restaurantes")
    restaurantes = cursor.fetchall()
    conn.close()
    return restaurantes

def obter_restaurantes_by_user(user_id = None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT r.id, r.nome FROM restaurantes r JOIN user_restaurante ur ON r.id = ur.restaurante_id WHERE ur.user_id=?", (int(get_usuario_id()),))

    restaurantes = cursor.fetchall()
    conn.close()
    return restaurantes

# Funções para Inserir restaurantes de Medida
def inserir_restaurante(nome):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO restaurantes (nome) VALUES (?)", (nome,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return e

def obter_restaurante_pelo_id(restaurante_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM restaurantes WHERE id=?", (int(restaurante_id),))
    restaurante = cursor.fetchone()
    conn.close()
    return restaurante

def definir_restaurantes_to_users(user_id, restaurantes):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_restaurante WHERE user_id=?", (user_id,))
    for restaurante in restaurantes:
        cursor.execute("INSERT INTO user_restaurante (user_id, restaurante_id) VALUES (?, ?)", (user_id, restaurante))
    conn.commit()
    conn.close()