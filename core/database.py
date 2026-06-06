import sqlite3
import os

DB_PATH = "highscores.db"

def initialize_db():
    """Erstellt die Datenbank und die Tabelle, falls noch nicht vorhanden."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS highscores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            score INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_score(user_name, score):
    """Speichert einen neuen High-Score."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO highscores (user_name, score) VALUES (?, ?)', (user_name, score))
    conn.commit()
    conn.close()

def get_best_score():
    """Holt den höchsten Score aus der Datenbank."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(score) FROM highscores')
    result = cursor.fetchone()[0]
    conn.close()
    return result if result is not None else 0

# Initialisiere die DB direkt beim Importieren, falls sie fehlt
initialize_db()