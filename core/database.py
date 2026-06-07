import sqlite3
import logging
from datetime import datetime

DB_PATH = "highscores.db"


def init_db():
    """Initialisiert die Datenbank und erstellt die Log-Tabelle, falls sie nicht existiert."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS agent_logs
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       timestamp TEXT NOT NULL,
                       original_text TEXT NOT NULL,
                       summary TEXT NOT NULL,
                       score INTEGER NOT NULL,
                       execution_time REAL NOT NULL
                   )
                   """)
    conn.commit()
    conn.close()


def get_all_time_highscore():
    """Holt den höchsten jemals erzielten Score aus allen Durchläufen."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MAX(score) FROM agent_logs")
        result = cursor.fetchone()[0]
        return result if result is not None else 0
    except sqlite3.OperationalError:
        return 0
    finally:
        conn.close()


def save_agent_run(original_text, summary, score, execution_time):
    """Speichert einen vollständigen Durchlauf des Agenten in der Datenbank."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
                   INSERT INTO agent_logs (timestamp, original_text, summary, score, execution_time)
                   VALUES (?, ?, ?, ?, ?)
                   """, (timestamp, original_text, summary, score, round(execution_time, 2)))

    conn.commit()
    conn.close()
    logging.info(f"💾 Durchlauf erfolgreich in Datenbank protokolliert (Dauer: {round(execution_time, 2)}s).")
