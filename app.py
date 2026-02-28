import streamlit as st
import requests
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
# Nota: Su Streamlit Cloud leggeremo la chiave in modo diverso (punto 4),
# ma questo codice va bene per entrambi.
api_key = os.getenv("API_KEY")
CHIAVE_GEMINI= os.getenv("GEMINI_KEY")

client= genai.Client(api_key=CHIAVE_GEMINI)


def chiamata(city, temp, desc):
    prompt=f"Sei un pappagallo simpatico. A {city} ci sono {temp} gradi e il tempo è {desc}. Commenta brevemente il tempo usando anche l'emoji del pappagallo"
    risposta=client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return risposta.text

st.set_page_config(page_title="Meteo App", page_icon="🌤️")

st.title("🌦️Il meteo del pappagallo🦜")
st.write("Inserisci il nome di una città per sapere che tempo fa.")

citta = st.text_input("Città", placeholder="Es: Roma")

if st.button("Controlla Meteo") or citta:
    if not api_key:
        st.error("Errore: Chiave API non trovata!")
    elif citta:
        with st.status(f"Volando verso {citta}...", expanded=True) as status:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={citta}&appid={api_key}&units=metric&lang=it"
            res = requests.get(url)
            if res.status_code == 200:
                dati = res.json()
                temp = dati["main"]["temp"]
                desc = dati["weather"][0]["description"]
                st.metric(label="Temperatura", value=f"{temp} °C")
                st.info(f"Condizioni: {desc.capitalize()}")
                st.write("Il pappagallo sta per dare la sua risposta...")
                ans_gem=chiamata(citta, temp, desc)
                status.update(label="Risposta pronta!", state="complete")

            else:
                st.error("Città non trovata. Riprova!")
        with st.chat_message("assistant", avatar="🦜"):
            if res.status_code == 200:
                st.write(ans_gem)
            else:
                st.error("Il pappagallo è scappato. Riprova!")
    else:
        st.warning("Per favore, inserisci il nome di una città.")