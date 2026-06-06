from agents.master_agent import MasterAgent


def start_system():
    print("🤖 --- Personal Agent System wird gestartet --- 🤖")
    print("Initialisiere Master-Agent...")

    # Master Agent wird zum Leben erweckt
    master = MasterAgent()

    print("\n✅ System bereit! Tippe 'exit' oder 'quit' zum Beenden.\n")

    # Endlosschleife für den Chat
    while True:
        user_input = input("User ➔ ")

        # Abbruchbedingung
        if user_input.lower() in ["exit", "quit"]:
            print("\n🤖 System wird heruntergefahren. Bis bald, Captain!")
            break

        # Wenn die Eingabe leer ist, ignorieren
        if not user_input.strip():
            continue

        # Agenten nach einer Antwort fragen
        print(f"⏳ {master.name} denkt nach...")
        reply = master.run(user_input)

        # Antwort ausgeben
        print(f"\n{master.name} ➔ {reply}\n")


if __name__ == "__main__":
    start_system()