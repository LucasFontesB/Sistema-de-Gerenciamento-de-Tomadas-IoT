import sqlite3
from flask import current_app

def init_db():
    with sqlite3.connect(current_app.config["DB_PATH"]) as conn:
        cursor = conn.cursor()

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

        conn.commit()