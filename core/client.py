import os
from dotenv import load_dotenv
from openai import OpenAI

# Lädt die API-Keys aus der .env-Datei im Hauptordner
load_dotenv()


def get_groq_client():
    """
    Erstellt und gibt einen vorkonfigurierten Client für die Groq-API zurück.
    Groq nutzt dieselbe Struktur wie OpenAI, weshalb wir das openai-Paket verwenden können.
    """
    api_key = os.getenv("GROQ_API_KEY")

    # Sicherheitscheck: Falls der Key vergessen wurde
    if not api_key or "hier_deinen_kopierten_schlüssel" in api_key:
        raise ValueError("❌ Fehler: GROQ_API_KEY wurde nicht korrekt in der .env-Datei eingetragen!")

    # Wir verbinden uns mit Groq, nutzen aber das superschnelle Llama-Modell
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )
    return client