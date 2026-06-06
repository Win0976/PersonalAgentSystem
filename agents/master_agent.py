import logging
import json


class MasterAgent:
    def __init__(self, client):
        """Initialisiert den Agenten mit dem konfigurierten Groq/OpenAI-Client."""
        self.client = client

    def execute_task(self, text_to_analyze):
        """
        Analysiert einen Text und bewertet die eigene Leistung mit der Power von Llama 70B.
        Gibt ein Tuple zurück: (Zusammenfassung, Score)
        """
        logging.info("Sende Anfrage an Groq für die Textanalyse (Llama 70B)...")

        prompt = (
            f"Analysiere und verfasse eine prägnante Zusammenfassung des folgenden Textes. "
            f"Bewerte danach deine eigene Zusammenfassung kritisch auf einer Skala von 1 bis 100 "
            f"(wie präzise, strukturiert und informativ ist sie wirklich?).\n"
            f"Gib das Ergebnis STRENGSTENS im folgenden JSON-Format aus, ohne zusätzlichen Text drumherum:\n"
            f'{{"zusammenfassung": "Deine Zusammenfassung hier", "score": 85}}\n\n'
            f"Text zum Analysieren:\n{text_to_analyze}"
        )

        try:
            # Upgrade auf das extrem mächtige 70B-Modell
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Das große, intelligente Modell für komplexe Logik
                messages=[
                    {"role": "system",
                     "content": "Du bist ein hochpräziser, kritischer Analyse-Agent, der ausnahmslos mit validem JSON antwortet."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Niedrige Temperatur für weniger Kreativität und mehr Faktenstreue
                response_format={"type": "json_object"}  # Erzwingt ein sauberes JSON-Objekt
            )

            # JSON-Antwort parsen
            raw_content = response.choices[0].message.content
            data = json.loads(raw_content)

            zusammenfassung = data.get("zusammenfassung", "Keine Zusammenfassung generiert.")
            score = int(data.get("score", 0))

            return zusammenfassung, score

        except Exception as e:
            logging.error(f"Fehler bei der Kommunikation mit der KI-API: {e}")
            # Fallback-Werte, falls etwas schiefgeht
            return "Fehler bei der Analyse.", 0