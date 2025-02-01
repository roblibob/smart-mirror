import sqlite3
from datetime import datetime

DB_PATH = "visits.db"

def init_db():
    """Initializes the SQLite database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            name TEXT PRIMARY KEY,
            last_seen TEXT
        )
    """)
    conn.commit()
    return conn, cursor

def update_last_seen(cursor, name):
    """Updates the last seen timestamp of a recognized person."""
    visit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO visits (name, last_seen) VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET last_seen=?", 
                   (name, visit_time, visit_time))
    cursor.connection.commit()

def get_last_seen(cursor, name):
    """Retrieves the last visit time of a recognized person."""
    cursor.execute("SELECT last_seen FROM visits WHERE name=?", (name,))
    row = cursor.fetchone()
    return row[0] if row else None