import streamlit as st
import json
import os
import pandas as pd
from agents.base_agent import BaseAgent

# --- KONFIGURATION & STATE ---
STATE_FILE = "imperium_state.json"


def save_state(ceo):
    data = {name: agent.system_prompt for name, agent in ceo.sub_agents.items()}
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def load_state(ceo):
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for name, prompt in data.items():
                    ceo.spawn_sub_agent(name, prompt)
        except:
            pass


# --- INITIALISIERUNG ---
if "ceo" not in st.session_state:
    st.session_state.ceo = BaseAgent(name="CEO-Master-Agent", system_prompt="Du bist der CEO des Lebens-Imperiums.")
    load_state(st.session_state.ceo)
    # Sicherstellen, dass die wichtigsten Agenten da sind
    board_members = {
        "Haushalts-Manager": "Experte für Haushaltsführung, Putzpläne und Einkaufsoptimierung.",
        "Finanz-Controller": "Experte für Budgetierung, Haushaltsbuch und Kostenkontrolle.",
        "Dräxlmaier-Mentor": "Ausbildungsbegleiter für Anwendungsentwickler bei Dräxlmaier (Vilsbiburg).",
        "DevSecOps-Coach": "Experte für Cloud-Infrastruktur, Security und Automatisierung.",
        "Gesundheits-Guru": "Experte für effiziente Ernährung, Fitness und Schlaf-Optimierung.",
        "Zeit-Produktivitäts-Agent": "Experte für Zeitmanagement und Aufgaben-Priorisierung.",
        "Travel-Logistik-Agent": "Experte für Reiseplanung und Mobilität zwischen Konstanz und Vilsbiburg.",
        "RechercheProfi": "Experte für Internet-Recherchen."
    }
    for name, role in board_members.items():
        if name not in st.session_state.ceo.sub_agents:
            st.session_state.ceo.spawn_sub_agent(name, role)
    save_state(st.session_state.ceo)

if "active_agent" not in st.session_state:
    st.session_state.active_agent = "CEO-Master-Agent"

# --- UI LAYOUT ---
st.set_page_config(page_title="KI-Imperium", layout="wide")

# Sidebar: Der "Baumstamm"
st.sidebar.title("🏢 Mein Imperium")

# CEO Button
if st.sidebar.button("👑 CEO-Master-Agent"):
    st.session_state.active_agent = "CEO-Master-Agent"

st.sidebar.markdown("---")
st.sidebar.subheader("Sub-Agenten")

# Baum-Struktur in der Sidebar
for name in sorted(st.session_state.ceo.sub_agents.keys()):
    if st.sidebar.button(f"👤 {name}"):
        st.session_state.active_agent = name

# Hauptbereich
st.title(f"Kommunikation mit: {st.session_state.active_agent}")

# Agent Logik Auswahl
if st.session_state.active_agent == "CEO-Master-Agent":
    current_agent = st.session_state.ceo
else:
    current_agent = st.session_state.ceo.sub_agents[st.session_state.active_agent]

# Chat Interface
if user_input := st.chat_input(f"Anweisung an {st.session_state.active_agent} senden..."):
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        # Wir rufen direkt den ausgewählten Agenten auf
        reply = current_agent.run(user_input)

        # Einfache Datenvisualisierung
        if "📊 DATEN:" in reply:
            try:
                text_vorher, rest = reply.split("📊 DATEN:", 1)
                json_teil, text_nachher = rest.split("}", 1)
                data = json.loads(json_teil + "}")
                st.write(text_vorher)
                st.bar_chart(pd.DataFrame(data).set_index("Labels"))
                st.write(text_nachher)
            except:
                st.write(reply)
        else:
            st.write(reply)

# Info Footer
st.sidebar.markdown("---")
st.sidebar.info(f"Status: Verbunden mit **{st.session_state.active_agent}**")