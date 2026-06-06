import sys
import logging
from agents.master_agent import MasterAgent
from core.client import initialize_client
from core.database import save_score, get_best_score

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_agent():
    logging.info("Starte Personal Agent System...")

    # 1. System initialisieren
    client = initialize_client()
    agent = MasterAgent(client)

    # Historischen Bestwert abrufen
    best_score = get_best_score()
    logging.info(f"Aktueller Highscore geladen: {best_score}")

    try:
        # Hier läuft deine Hauptlogik
        # Beispiel: Agent führt eine Aufgabe aus
        result = agent.execute_task("Führe Analyse durch")

        # Angenommen, dein Agent gibt ein Ergebnis zurück, das einen Score hat
        # Hier beispielhaft ein Score von 100 (ersetze das durch deine echte Logik)
        current_score = 100

        if current_score > best_score:
            logging.info(f"Neuer Highscore erreicht: {current_score} (Vorher: {best_score})")
            save_score("Hauptnutzer", current_score)
        else:
            logging.info(f"Ergebnis: {current_score}. Highscore von {best_score} nicht übertroffen.")

    except Exception as e:
        logging.error(f"Fehler während der Ausführung: {e}")
        sys.exit(1)

    logging.info("Programmablauf beendet.")


if __name__ == "__main__":
    run_agent()