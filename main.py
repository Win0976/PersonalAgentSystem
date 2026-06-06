import logging
import time
from core.database import init_db, get_all_time_highscore, save_agent_run
from core.client import get_groq_client
from agents.master_agent import MasterAgent
from agents.reviewer_agent import ReviewerAgent  # Unser Neuzugang!

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("Starte Multi-Agenten-Tribunal...")

    init_db()
    client = get_groq_client()

    # Beide Agenten initialisieren
    master_agent = MasterAgent(client)
    reviewer_agent = ReviewerAgent(client)

    old_highscore = get_all_time_highscore()
    print("\n" + "=" * 60)
    print(f" 🏆  AKTUELLER ALL-TIME-HIGHSCORE: {old_highscore} Punkte")
    print("=" * 60 + "\n")

    print("Füge hier den Text ein, den das Tribunal analysieren soll:")
    text_to_analyze = input("> ").strip()

    if not text_to_analyze:
        logging.info("Kein Text eingegeben. Nutze Standard-Fallback-Text.")
        text_to_analyze = (
            "Das Multi-Agenten-Tribunal trennt strikt zwischen Generierung und Evaluation. "
            "Während der MasterAgent die kreative Arbeit leistet, überwacht der ReviewerAgent "
            "die Einhaltung aller Qualitäts- und Sicherheitsstandards. Dies minimiert KI-Halluzinationen."
        )

    print("\n" + "-" * 60)

    # Zeitmessung für die gesamte Pipeline starten
    start_time = time.time()

    # Phase 1: Master-Agent generiert die Zusammenfassung
    logging.info("[Phase 1] Master-Agent startet Textanalyse...")
    summary = master_agent.execute_task(text_to_analyze)
    logging.info(f"-> Ergebnis Master-Agent: '{summary}'")

    # Phase 2: Reviewer-Agent bewertet die Arbeit des Master-Agenten
    logging.info("[Phase 2] Übergabe an Reviewer-Agent zur unbestechlichen Bewertung...")
    score = reviewer_agent.evaluate_summary(text_to_analyze, summary)
    logging.info(f"-> Urteil des Reviewers: {score}/100 Punkte")

    execution_time = time.time() - start_time

    # Ergebnisse in die Analytics-DB wegsichern
    save_agent_run(text_to_analyze, summary, score, execution_time)

    # Highscore-Check
    if score > old_highscore:
        logging.info(f"🔥 NEUER ALL-TIME-HIGHSCORE: {score} Punkte! (Kritiker war beeindruckt!)")
    else:
        logging.info(f"Highscore von {old_highscore} Punkten wurde vom Reviewer nicht vergeben.")

    logging.info(f"Gesamtdauer des Tribunals: {round(execution_time, 2)}s. Beendet.")


if __name__ == "__main__":
    main()