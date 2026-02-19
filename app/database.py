import sqlite3
from flask import current_app

def init_db():
    with sqlite3.connect(current_app.config["DB_PATH"]) as conn:
        cursor = conn.cursor()

        # Tabela de dispositivos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dispositivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                apartamento TEXT NOT NULL,
                device_id TEXT NOT NULL,
                local_key TEXT NOT NULL,
                ip TEXT NOT NULL,
                version REAL NOT NULL
            )
        """)

        # Tabela de consumo
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consumo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dispositivo_id INTEGER NOT NULL,
                potencia REAL,
                corrente REAL,
                tensao REAL,
                energia_kwh REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(dispositivo_id)
                    REFERENCES dispositivos(id)
                    ON DELETE CASCADE
            )
        """)

        conn.commit()
