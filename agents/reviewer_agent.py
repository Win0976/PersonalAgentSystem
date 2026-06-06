import logging


class ReviewerAgent:
    def __init__(self, client):
        self.client = client
        self.model = "llama-3.3-70b-versatile"

    def evaluate_summary(self, original_question, teacher_answer):
        """Prüft die Antwort des Lehrers gegen die ursprüngliche Frage des Schülers."""
        logging.info("Prüfungsausschuss (Reviewer) bewertet die Lehrer-Antwort...")

        system_prompt = (
            "Du bist ein unbestechlicher Prüfer für IT-Ausbildungen. Deine Aufgabe ist es, "
            "die Antwort eines IT-Lehrers kritisch gegen die Frage des Schülers zu prüfen. "
            "Bewerte die Qualität knallhart nach folgenden Kriterien:\n"
            "1. Fachliche Korrektheit (Sind die IT-Fakten fehlerfrei?)\n"
            "2. Verständlichkeit (Ist es perfekt für einen Azubi erklärt?)\n"
            "3. Mehrwert (Hilft die Antwort dem Schüler wirklich weiter?)\n\n"
            "Antworte AUSSCHLIESSLICH mit einer Ganzzahl zwischen 1 und 100. "
            "Kein Text, keine Erklärung. Nur die nackte Zahl."
        )

        user_content = f"FRAGE DES SCHÜLERS:\n{original_question}\n\nANTWORT DES LEHRERS:\n{teacher_answer}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.1
        )

        raw_score = response.choices[0].message.content.strip()

        try:
            score = int(''.join(filter(str.isdigit, raw_score)))
            return min(max(score, 1), 100)
        except ValueError:
            return 50