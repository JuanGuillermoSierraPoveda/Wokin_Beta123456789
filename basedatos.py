# database.py

import sqlite3

def conectar():
    return sqlite3.connect("usuarios.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def registrar_usuario(username, password):
    crear_tabla()   # asegura que exista
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verificar_usuario(username, password):
    crear_tabla()   # asegura que exista
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

# 🚨 NUEVAS FUNCIONES PARA OBTENER Y ACTUALIZAR
def obtener_usuario_por_username(username):
    crear_tabla()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM usuarios WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        # Retorna un diccionario para fácil acceso
        return {"id": user_data[0], "username": user_data[1], "password": user_data[2]}
    return None

def actualizar_username(old_username, new_username):
    crear_tabla()
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE usuarios SET username = ? WHERE username = ?", (new_username, old_username))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True si se actualizó al menos una fila
    except sqlite3.IntegrityError:
        # Si el nuevo username ya existe
        return False
    finally:
        conn.close()

def actualizar_password(username, new_password):
    crear_tabla()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET password = ? WHERE username = ?", (new_password, username))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0 # Retorna True si se actualizó al menos una fila