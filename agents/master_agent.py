import logging


class MasterAgent:
    def __init__(self, client):
        self.client = client
        self.model = "llama-3.3-70b-versatile"

    def execute_task(self, text):
        """Generiert exklusiv eine prägnante Zusammenfassung des Textes."""
        logging.info("Sende Anfrage an Groq für die Textanalyse (Llama 70B)...")

        system_prompt = (
            "Du bist der Master-Agent. Deine Aufgabe ist es, den bereitgestellten Text präzise, "
            "klar und professionell in einem einzigen, dichten Satz zusammenzufassen. "
            "Antworte AUSSCHLIESSLICH mit dieser Zusammenfassung, ohne Einleitung oder Metatext."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )

        summary = response.choices[0].message.content.strip()
        return summary