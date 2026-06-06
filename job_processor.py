import os
import time
from agents.base_agent import BaseAgent

# CEO Agent initialisieren
ceo = BaseAgent(name="CEO-Master-Agent",
                system_prompt="Du bist der CEO. Deine Aufgabe ist es, Aufgaben aus Dateien abzuarbeiten.")

AUFGABEN_ORDNER = "aufgaben_warteschlange"
ARCHIV_ORDNER = "imperium_archiv"


def verarbeite_aufgaben():
    if not os.path.exists(AUFGABEN_ORDNER):
        os.makedirs(AUFGABEN_ORDNER)
        print(f"📁 Ordner '{AUFGABEN_ORDNER}' erstellt. Bitte lege hier deine Aufgaben-Dateien ab.")
        return

    # Suche nach .txt Dateien im Aufgaben-Ordner
    dateien = [f for f in os.listdir(AUFGABEN_ORDNER) if f.endswith(".txt")]

    for datei in dateien:
        pfad = os.path.join(AUFGABEN_ORDNER, datei)

        print(f"🚀 Verarbeite Aufgabe: {datei}...")

        # Inhalt lesen
        with open(pfad, "r", encoding="utf-8") as f:
            aufgabe = f.read()

        # Aufgabe an den CEO geben
        ergebnis = ceo.run(aufgabe)

        # Ergebnis im Archiv speichern
        ergebnis_datei = f"ergebnis_{datei}"
        with open(os.path.join(ARCHIV_ORDNER, ergebnis_datei), "w", encoding="utf-8") as f:
            f.write(ergebnis)

        print(f"✅ Fertig! Ergebnis gespeichert unter: {ergebnis_datei}")

        # Aufgabe löschen (damit sie nicht doppelt ausgeführt wird)
        os.remove(pfad)


if __name__ == "__main__":
    print("🤖 Job-Prozessor gestartet. Warte auf Befehle...")
    while True:
        verarbeite_aufgaben()
        time.sleep(10)  # Prüft alle 10 Sekunden