import os
from datetime import datetime
from core.client import get_groq_client
from ddgs import DDGS
from core.memory import MemorySystem


class BaseAgent:
    def __init__(self, name: str, system_prompt: str, model: str = "llama-3.3-70b-versatile"):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model
        self.client = get_groq_client()
        self.sub_agents = {}
        self.memory = MemorySystem()

    def spawn_sub_agent(self, name: str, task_prompt: str):
        if name not in self.sub_agents:
            self.sub_agents[name] = BaseAgent(name=name, system_prompt=task_prompt, model=self.model)
            print(f"👑 [{self.name}] hat einen neuen Spezialisten-Agenten erschaffen: '{name}'")
        return self.sub_agents[name]

    def search_internet(self, query: str) -> str:
        try:
            print(f"🌐 Live-Suche aktiv: [{self.name}] sucht nach '{query}'...")
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
            if not results: return "Keine aktuellen Internet-Ergebnisse gefunden."
            formatted_results = "\n".join(
                [f"[{i + 1}] {r['title']}\nQuelle: {r['href']}\n{r['body']}" for i, r in enumerate(results)])
            return formatted_results
        except Exception as e:
            return f"Fehler bei der Websuche: {e}"

    def write_file(self, filename: str, content: str) -> str:
        try:
            if not os.path.exists("imperium_archiv"): os.makedirs("imperium_archiv")
            path = os.path.join("imperium_archiv", filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"✅ Datei unter {path} gespeichert!"
        except Exception as e:
            return f"Fehler beim Schreiben der Datei: {e}"

    def run(self, user_input: str) -> str:
        try:
            jetzt = datetime.now().strftime("%d.%m.%Y um %H:%M:%S Uhr")
            imperium_regeln = (
                f"\n\n[System-Zeit: {jetzt}]. Aktive Unter-Agenten: {list(self.sub_agents.keys())}.\n"
                "WERKZEUGE - VERFAHRENSWEISE:\n"
                "1. PRÜFE IMMER ZUERST dein Wissens-Gedächtnis mit 'ABRUFEN: Suchbegriff', wenn der Nutzer eine Wissensfrage stellt.\n"
                "2. Suche erst dann im Internet mit 'SUCHE: Suchbegriff', wenn dein Gedächtnis keine ausreichende Antwort liefert.\n"
                "3. Archivierung: 'SCHREIBE_DATEI: name.txt | Inhalt' (Nur für große Dokumente).\n"
                "4. Lernen: 'SPEICHERN: Inhalt' (Wichtige neue Erkenntnisse sofort speichern).\n"
                "5. Delegation: 'BEFEHL: Name | System-Rolle | Aufgabe'."
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": f"{self.system_prompt}{imperium_regeln}"},
                          {"role": "user", "content": user_input}],
                temperature=0.7
            )
            reply = response.choices[0].message.content

            # Tool-Parser
            if "SUCHE:" in reply:
                suchbegriff = reply.split("SUCHE:")[1].strip().strip("'\"")
                ergebnis = self.search_internet(suchbegriff)
                return self.run(f"Hier sind die Suchergebnisse: {ergebnis}. Fasse sie zusammen oder verarbeite sie.")

            elif "SCHREIBE_DATEI:" in reply:
                parts = reply.split("SCHREIBE_DATEI:")[1].split("|")
                return self.write_file(parts[0].strip(), "|".join(parts[1:]).strip())

            elif "BEFEHL:" in reply:
                try:
                    parts = reply.split("BEFEHL:")[1].split("|")
                    name, rolle, aufgabe = parts[0].strip(), parts[1].strip(), parts[2].strip()
                    sub_agent = self.spawn_sub_agent(name, rolle)
                    print(f"⚡ Delegation an {name}: {aufgabe}")
                    ergebnis = sub_agent.run(aufgabe)
                    return f"Ergebnis von {name}: {ergebnis}"
                except Exception as e:
                    return f"Delegations-Fehler: {e}"

            elif "SPEICHERN:" in reply:
                inhalt = reply.split("SPEICHERN:")[1].strip()
                self.memory.speichern(inhalt)
                return f"🧠 Gedächtnis-Eintrag erfolgreich gespeichert: '{inhalt[:50]}...'"

            elif "ABRUFEN:" in reply:
                suchbegriff = reply.split("ABRUFEN:")[1].strip()
                erinnerungen = self.memory.abrufen(suchbegriff)
                # Hier führen wir den Abruf aus und senden das Ergebnis direkt zurück an den LLM
                return self.run(
                    f"Ich habe folgende Erinnerungen zu '{suchbegriff}' gefunden: {erinnerungen}. Verarbeite diese und beantworte die Nutzeranfrage.")

            return reply
        except Exception as e:
            return f"❌ [{self.name}] Fehler: {e}"