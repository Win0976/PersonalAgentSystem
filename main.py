import logging
import time
from typing import Tuple

# Hier importieren wir alle Core-Komponenten und Agenten sauber ein
from core.client import get_groq_client
from core.database import save_agent_run, get_all_time_highscore
from agents.master_agent import MasterAgent
from agents.reviewer_agent import ReviewerAgent

# --- KONSTANTEN ---
DEFAULT_PROMPT = "Zeig mir, was du kannst, Lehrer-Agent!"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


def setup_logging() -> None:
    """Initialisiert das System-Logging im Terminal."""
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def get_user_input() -> str:
    """Liest die Frage des Benutzers ein oder liefert den Standard-Text."""
    print("\n" + "=" * 60)
    user_text = input("Füge hier den Text ein, den das Tribunal analysieren soll:\n> ")
    print("=" * 60 + "\n")

    return user_text.strip() if user_text.strip() else DEFAULT_PROMPT


def run_tribunal(master_agent: MasterAgent, reviewer_agent: ReviewerAgent, text: str) -> Tuple[str, int]:
    """Orchestriert die beiden Phasen des Tribunals (Lehrer & Prüfer)."""
    # Phase 1: Der Lehrer-Agent erklärt
    logging.info("[Phase 1] Master-Agent startet Textanalyse...")
    teacher_answer = master_agent.execute_task(text)
    logging.info(f"-> Ergebnis Master-Agent: '{teacher_answer}'")

    # Phase 2: Der unbestechliche Prüfer bewertet
    logging.info("[Phase 2] Übergabe an Reviewer-Agent zur unbestechlichen Bewertung...")
    score = reviewer_agent.evaluate_summary(text, teacher_answer)
    logging.info(f"-> Urteil des Reviewers: {score}/100 Punkte")

    return teacher_answer, score


def evaluate_highscore(current_score: int) -> None:
    """Holt den allzeit Highscore aus der DB und prüft, ob er geknackt wurde."""
    highscore = get_all_time_highscore()
    if current_score >= highscore:
        logging.info(f"🏆 NEUER HIGHSCORE! Du hast den alten Highscore von {highscore} Punkten geschlagen!")
    else:
        logging.info(f"Highscore von {highscore} Punkten wurde vom Reviewer nicht vergeben.")


# --- HAUPTPROGRAMM ---
def main() -> None:
    setup_logging()

    # Initialisierung der Core-Komponenten
    client = get_groq_client()
    master_agent = MasterAgent(client)
    reviewer_agent = ReviewerAgent(client)

    # Input holen
    text_to_analyze = get_user_input()

    # Zeitmessung starten & Tribunal ausführen
    start_time = time.time()
    teacher_answer, score = run_tribunal(master_agent, reviewer_agent, text_to_analyze)
    duration = round(time.time() - start_time, 2)

    # Daten speichern & Highscore prüfen
    save_agent_run(text_to_analyze, teacher_answer, score, duration)
    evaluate_highscore(score)

    logging.info(f"Gesamtdauer des Tribunals: {duration}s. Beendet.")


if __name__ == "__main__":
    main()