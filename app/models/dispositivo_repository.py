import sqlite3
from flask import current_app

def listar_dispositivos():
    with sqlite3.connect(current_app.config["DB_PATH"]) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute("SELECT * FROM dispositivos").fetchall()

def buscar_por_id(id):
    with sqlite3.connect(current_app.config["DB_PATH"]) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(
            "SELECT * FROM dispositivos WHERE id=?",
            (id,)
        ).fetchone()

def inserir_dispositivo(dados):
    with sqlite3.connect(current_app.config["DB_PATH"]) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dispositivos (apartamento, device_id, local_key, ip, version)
            VALUES (?, ?, ?, ?, ?)
        """, (
            dados["apartamento"],
            dados["device_id"],
            dados["local_key"],
            dados["ip"],
            float(dados["version"])
        ))

        novo_id = cursor.lastrowid
        conn.commit()

    return novo_id

def atualizar_dispositivo(id, dados):
    with sqlite3.connect(current_app.config["DB_PATH"]) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE dispositivos
            SET apartamento = ?,
                device_id = ?,
                local_key = ?,
                ip = ?,
                version = ?
            WHERE id = ?
        """, (
            dados["apartamento"],
            dados["device_id"],
            dados["local_key"],
            dados["ip"],
            float(dados["version"]),
            id
        ))
        conn.commit()

def deletar_dispositivo(id):
    with sqlite3.connect(current_app.config["DB_PATH"]) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM dispositivos WHERE id = ?", (id,))
        if cursor.fetchone() is None:
            return False

        cursor.execute("DELETE FROM dispositivos WHERE id = ?", (id,))
        conn.commit()
        return True