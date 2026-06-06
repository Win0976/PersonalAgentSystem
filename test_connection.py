from core.client import get_groq_client


def test_api():
    try:
        print("⏳ Teste Verbindung zu Groq mitaktuellem Modell...")
        client = get_groq_client()

        # Hier nutzen wir jetzt das aktuelle Llama 3.1 Modell von Groq
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "Antworte mir exakt mit den Worten: 'System bereit, Captain!'"}
            ],
            max_tokens=20
        )

        print("\n🎉 ERFOLG! Deine Leitung steht bombenfest!")
        print(f"Antwort von Groq: {response.choices[0].message.content}")

    except Exception as e:
        print("\n❌ Fehler beim Verbindungstest!")
        print(f"Details: {e}")


if __name__ == "__main__":
    test_api()