import os
import sys
import logging
from dotenv import load_dotenv
from agents.master_agent import MasterAgent
from core.client import initialize_client
from core.database import save_score, get_best_score

# 1. Konfiguration laden (MUSS vor allem anderen passieren!)
# Sucht nach einer .env Datei im Projektverzeichnis und lädt die Variablen in das OS-Environment
load_dotenv()

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_agent():
    logging.info("Starte Personal Agent System mit Umgebungskonfiguration...")

    # Sicherheits-Check: Prüfen, ob wichtige Variablen geladen wurden
    # Ersetze 'GROQ_API_KEY' durch den exakten Namen deiner Variable in der .env, falls er anders heißt
    if not os.getenv("GROQ_API_KEY"):
        logging.error("Kritischer Fehler: GROQ_API_KEY wurde in der Umgebung nicht gefunden!")
        logging.error("Bitte stelle sicher, dass eine .env-Datei mit dem Key existiert.")
        sys.exit(1)

    # 2. System initialisieren
    # Der Client zieht sich den API-Key jetzt automatisch und sicher aus dem Betriebssystem
    client = initialize_client()
    agent = MasterAgent(client)

    # Historischen Bestwert aus der SQLite-DB abrufen
    best_score = get_best_score()
    logging.info(f"Aktueller Highscore geladen: {best_score}")

    try:
        # Hauptlogik des Agenten ausführen
        result = agent.execute_task("Führe Analyse durch")

        # Beispielhafter Score zur Demonstration der Speicher-Logik
        current_score = 100

        if current_score > best_score:
            logging.info(f"Neuer Highscore erreicht: {current_score} (Vorher: {best_score})")
            save_score("Hauptnutzer", current_score)
        else:
            logging.info(f"Ergebnis: {current_score}. Highscore von {best_score} nicht übertroffen.")

    except Exception as e:
        logging.error(f"Fehler während der Ausführung: {e}")
        sys.exit(1)

    logging.info("Programmablauf erfolgreich beendet.")


if __name__ == "__main__":
    run_agent()