import sqlite3
import hashlib
from utils.get_globals import set_usuario_id
from utils.get_globals import get_dbpath

# Caminho do banco de dados
dbpath = get_dbpath()

def conectar():
    return sqlite3.connect(dbpath)

def verificar_login(login, senha):
    conn = conectar()
    cursor = conn.cursor()
    
    # Verificar login e senha
    senha = hashlib.md5(senha.encode()).hexdigest()
    consulta = 'SELECT * FROM usuarios WHERE login = ? AND senha = ?'
    cursor.execute(consulta, (login, senha))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario:
        set_usuario_id(None)
        return False
    else:
        set_usuario_id(usuario[0])
        return True

def obter_usuario_by_login(login):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE login = ?", (login,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def obter_usuario_by_id(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def obter_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, login FROM usuarios order by id")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def alterar_senha(user_id, senha):
    conn = conectar()
    cursor = conn.cursor()
    senha = hashlib.md5(senha.encode()).hexdigest()
    cursor.execute("UPDATE usuarios SET senha = ? WHERE id = ?", (senha, user_id))
    conn.commit()
    conn.close()

def inserir_usuario(login, senha):
    conn = conectar()
    cursor = conn.cursor()
    senha = hashlib.md5(senha.encode()).hexdigest()
    cursor.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", (login, senha))
    conn.commit()
    conn.close()

def excluir_usuario(user_id):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=?", (int(user_id),))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return e

def obter_user_restaurante_by_id(user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT restaurante_id FROM user_restaurante where user_id = ?", (user_id,))
    user_restaurante = cursor.fetchall()
    conn.close()
    return user_restaurante

def alterar_permissoes(user_id, restaurantes):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_restaurante WHERE user_id = ?", (int(user_id),))
    for restaurante in restaurantes:
        cursor.execute("INSERT INTO user_restaurante (user_id, restaurante_id) VALUES (?, ?)", (int(user_id), restaurante))
    conn.commit()
    conn.close()