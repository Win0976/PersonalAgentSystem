import logging
import json
from tools.file_tools import read_local_file


class MasterAgent:
    def __init__(self, client):
        self.client = client
        self.model = "llama-3.3-70b-versatile"

    def execute_task(self, user_question):
        """Beantwortet Fragen und nutzt autonom Tools, falls der User eine Datei analysieren möchte."""
        logging.info("Lehrer-Agent analysiert die Anfrage...")

        system_prompt = (
            "Du bist der absolute Lieblingslehrer und Mentor für einen angehenden Fachinformatiker "
            "für Anwendungsentwicklung. Du bist herzlich, motivierend und fachlich brillant. "
            "Wenn der Schüler dich nach dem Inhalt einer Datei fragt oder Code aus einer Datei prüfen möchte, "
            "musst du das Werkzeug `read_local_file` aufrufen. "
            "Wichtig: Antworte bei einem Werkzeugaufruf NIEMALS mit normalem Text, sondern überlasse das "
            "vollständig der Tool-Schnittstelle."
        )

        tools = [{
            "type": "function",
            "function": {
                "name": "read_local_file",
                "description": "Liest den Inhalt einer lokalen Datei (z.B. main.py, .gitignore, Java-Dateien) ein.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Der exakte Dateiname oder Pfad auf der Festplatte (z.B. 'main.py')."
                        }
                    },
                    "required": ["file_path"]
                }
            }
        }]

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ]

        # 1. Aufruf mit Temp 0.0 -> Garantiert einen sauberen, fehlerfreien Tool-Aufruf bei Groq
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.0
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            logging.info("🤖 Agent hat entschieden, ein Werkzeug zu nutzen!")
            messages.append(response_message)

            for tool_call in tool_calls:
                if tool_call.function.name == "read_local_file":
                    function_args = json.loads(tool_call.function.arguments)
                    file_path = function_args.get("file_path")

                    logging.info(f"📂 Führe Tool 'read_local_file' für Pfad aus: {file_path}")
                    tool_output = read_local_file(file_path)

                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": "read_local_file",
                        "content": tool_output
                    })

            # 2. Aufruf: Hier kriegt die KI die Daten und darf vollkommen frei und herzlich antworten
            logging.info("Lehrer-Agent wertet den Dateiinhalt aus...")
            final_response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )
            return final_response.choices[0].message.content.strip()

        return response_message.content.strip()