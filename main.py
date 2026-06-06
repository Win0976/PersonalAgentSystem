import logging
import time
from core.database import init_db, get_all_time_highscore, save_agent_run
from core.client import get_groq_client
from agents.master_agent import MasterAgent

# Logging-Konfiguration für saubere Terminal-Ausgaben
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("Starte Personal Agent System mit interaktiver Texteingabe...")

    # 1. Datenbank & Client initialisieren
    init_db()
    client = get_groq_client()
    agent = MasterAgent(client)

    # 2. All-Time-Highscore laden & schick anzeigen
    old_highscore = get_all_time_highscore()
    print("\n" + "=" * 60)
    print(f" 🏆  AKTUELLER ALL-TIME-HIGHSCORE: {old_highscore} Punkte")
    print("=" * 60 + "\n")

    # 3. Dynamische Texteingabe über das Terminal abfragen
    print("Füge hier den Text ein, den der Agent analysieren soll:")
    text_to_analyze = input("> ").strip()

    # Falls der User einfach nur ENTER drückt, nutzen wir einen Fallback-Text
    if not text_to_analyze:
        logging.info("Kein Text eingegeben. Nutze Standard-Fallback-Text.")
        text_to_analyze = (
            "Ein angehender Anwendungsentwickler, der Git-Push-Protections bezwingt, "
            "Secrets über .gitignore maskiert und ein Llama-3.3-70B-Logging-System "
            "aufbaut, bringt verdammt starke Voraussetzungen für die DevSecOps-Welt mit."
        )

    print("\n" + "-" * 60)
    logging.info("Agent startet die Textanalyse und Selbstbewertung...")

    # Metrik: Zeitmessung starten
    start_time = time.time()

    # 4. Agent mit dem dynamischen Text ausführen
    summary, score = agent.execute_task(text_to_analyze)

    # Metrik: Zeitmessung stoppen
    execution_time = time.time() - start_time

    # 5. Ergebnisse loggen und in der DB sichern
    logging.info(f"Analyse-Ergebnis: {summary}")
    logging.info(f"Vom Agenten selbst vergebener Performance-Score: {score}/100")

    # Kompletten Datensatz in der erweiterten DB speichern
    save_agent_run(text_to_analyze, summary, score, execution_time)

    # 6. Highscore-Logik prüfen
    if score > old_highscore:
        logging.info(f"🔥 NEUER ALL-TIME-HIGHSCORE ERREICHT: {score} Punkte! (Vorher: {old_highscore})")
    else:
        logging.info(f"Ergebnis stabil. Der Highscore von {old_highscore} Punkten wurde nicht geschlagen.")

    logging.info("Programmablauf erfolgreich beendet.")


if __name__ == "__main__":
    main()