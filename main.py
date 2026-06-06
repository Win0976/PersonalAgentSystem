import os
import sys
import logging
from dotenv import load_dotenv
from agents.master_agent import MasterAgent
from core.client import get_groq_client  # Exakt auf deinen Client angepasst!
from core.database import save_score, get_best_score

# 1. Konfiguration laden
load_dotenv()

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_agent():
    logging.info("Starte Personal Agent System mit KI-Feedback-Schleife...")

    # Sicherheits-Check für API-Key
    if not os.getenv("GROQ_API_KEY"):
        logging.error("Kritischer Fehler: GROQ_API_KEY wurde in der Umgebung nicht gefunden!")
        sys.exit(1)

    try:
        # 2. System mit deinem echten Groq-Client initialisieren
        client = get_groq_client()
        agent = MasterAgent(client)

        # Historischen Bestwert aus der SQLite-DB abrufen
        best_score = get_best_score()
        logging.info(f"Aktueller Highscore geladen: {best_score}")

        # Ein echter, komplexer Text, den der Agent analysieren soll
        test_text = (
            "Künstliche Intelligenz revolutioniert die Softwareentwicklung. "
            "Durch automatisierte Pipelines (CI/CD) und den Einsatz von lokalen "
            "Sprachmodellen können Entwickler repetitive Aufgaben automatisieren "
            "und sich auf die Architektur konzentrieren. Die Sicherheit von API-Keys "
            "bleibt dabei eine der größten Herausforderungen im DevSecOps-Bereich."
        )

        logging.info("Agent startet die Textanalyse und Selbstbewertung...")

        # Der Agent führt die Aufgabe aus UND bewertet seine eigene Leistung
        analysis_result, current_score = agent.execute_task(test_text)

        logging.info(f"Analyse-Ergebnis: {analysis_result}")
        logging.info(f"Vom Agenten selbst vergebener Performance-Score: {current_score}/100")

        # Highscore-Logik mit echten Werten aus der Feedback-Schleife
        if current_score > best_score:
            logging.info(f"🔥 Neuer Highscore erreicht: {current_score} Punkten! (Vorher: {best_score})")
            save_score("MasterAgent_v1", current_score)
        else:
            logging.info(f"Ergebnis stabil. Der Highscore von {best_score} Punkten wurde nicht geschlagen.")

    except Exception as e:
        logging.error(f"Fehler während der Ausführung: {e}")
        sys.exit(1)

    logging.info("Programmablauf erfolgreich beendet.")


if __name__ == "__main__":
    run_agent()