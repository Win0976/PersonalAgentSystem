import logging


class ReviewerAgent:
    def __init__(self, client):
        self.client = client
        self.model = "llama-3.3-70b-versatile"

    def evaluate_summary(self, original_text, summary):
        """Vergleicht die Zusammenfassung mit dem Originaltext und vergibt einen Score."""
        logging.info("Sende Daten an den Reviewer-Agenten zur Qualitätskontrolle...")

        system_prompt = (
            "Du bist ein unbestechlicher Qualitätskontroll-Agent (Reviewer). Deine Aufgabe ist es, "
            "eine Zusammenfassung kritisch gegen den Originaltext zu prüfen. Bewerte die Qualität anhand von:\n"
            "1. Genauigkeit (Wurden Fakten verfälscht?)\n"
            "2. Vollständigkeit (Fehlen Kernpunkte?)\n"
            "3. Prägnanz (Ist es kurz und knackig?)\n\n"
            "Antworte AUSSCHLIESSLICH mit einer Ganzzahl zwischen 1 und 100. "
            "Kein Text, keine Erklärung, kein 'Score:'. Nur die nackte Zahl."
        )

        user_content = f"ORIGINALTEXT:\n{original_text}\n\nZUSAMMENFASSUNG DES MASTER-AGENTEN:\n{summary}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.1  # Sehr niedrige Temperatur für extrem konsistente, kritische Bewertung
        )

        raw_score = response.choices[0].message.content.strip()

        # Sicherstellen, dass wir nur die Zahl extrahieren
        try:
            score = int(''.join(filter(str.isdigit, raw_score)))
            return min(max(score, 1), 100)  # Garantiert einen Wert zwischen 1 und 100
        except ValueError:
            logging.warning(f"Reviewer lieferte ungültiges Format '{raw_score}'. Fallback auf 50.")
            return 50