import sqlite3

DB_PATH = "app.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        with open("schema.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.execute(
            "INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')"
        )
        conn.commit()
