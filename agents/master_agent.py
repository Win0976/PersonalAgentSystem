import logging


class MasterAgent:
    def __init__(self, client):
        self.client = client
        self.model = "llama-3.3-70b-versatile"

    def execute_task(self, user_question):
        """Beantwortet die Frage des Users als herzlicher und kompetenter IT-Lehrer."""
        logging.info("Lehrer-Agent bereitet die Erklärung vor...")

        system_prompt = (
            "Du bist der absolute Lieblingslehrer und Mentor für einen angehenden Fachinformatiker "
            "für Anwendungsentwicklung. Du bist extrem kompetent, herzlich, motivierend und geduldig. "
            "Deine Aufgabe ist es, die Frage des Schülers verständlich, professionell und mit einer "
            "positiven Energie zu beantworten. Nutze bei Bedarf einfache Analogien, lobe den Schüler für "
            "gute Fragen und sporne ihn an. Antworte direkt, freundlich und ohne Metatext."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0.7  # Etwas höher für mehr Empathie und Kreativität in der Sprache
        )

        answer = response.choices[0].message.content.strip()
        return answer