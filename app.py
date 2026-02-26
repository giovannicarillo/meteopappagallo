import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Nota: Su Streamlit Cloud leggeremo la chiave in modo diverso (punto 4),
# ma questo codice va bene per entrambi.
api_key = os.getenv("API_KEY")

st.set_page_config(page_title="Meteo App", page_icon="🌤️")

st.title("🌦️ La mia prima App Meteo")
st.write("Inserisci il nome di una città per sapere che tempo fa.")

citta = st.text_input("Città", placeholder="Es: Roma")

if st.button("Controlla Meteo"):
    if not api_key:
        st.error("Errore: Chiave API non trovata!")
    elif citta:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={citta}&appid={api_key}&units=metric&lang=it"
        res = requests.get(url)
        if res.status_code == 200:
            dati = res.json()
            temp = dati["main"]["temp"]
            desc = dati["weather"][0]["description"]
            st.metric(label="Temperatura", value=f"{temp} °C")
            st.info(f"Condizioni: {desc.capitalize()}")
        else:
            st.error("Città non trovata. Riprova!")
    else:
        st.warning("Per favore, inserisci il nome di una città.")