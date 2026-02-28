import streamlit as st
import requests
import os
from dotenv import load_dotenv
from google import genai
from groq import Groq

st.markdown("""
    <style>
    /* Nasconde il quadratino 'Running...' in alto a destra */
    [data-testid="stStatusWidget"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Nasconde il badge Running in alto a destra e quello vicino ai tasti */
    [data-testid="stStatusWidget"], 
    .stStatusWidget, 
    [data-testid="stStatusWidget"] div {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* Rimuove l'animazione di caricamento specifica dei bottoni nuovi */
    button div[data-testid="stMarkdownContainer"] ~ div {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)


load_dotenv()
# Nota: Su Streamlit Cloud leggeremo la chiave in modo diverso (punto 4),
# ma questo codice va bene per entrambi.
api_key = os.getenv("API_KEY")
CHIAVE_GEMINI= os.getenv("GEMINI_KEY")
client_groq = Groq(api_key=os.getenv("GROQ_KEY"))

client= genai.Client(api_key=CHIAVE_GEMINI)

def prendi_previsioni(citta, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={citta}&appid={api_key}&units=metric&lang=it"
    res = requests.get(url)

    if res.status_code == 200:
        dati = res.json()
        lista_previsioni = []

        # Prendiamo solo i primi 4 risultati (prossime 12 ore)
        for previsione in dati['list'][:4]:
            ora = previsione['dt_txt'].split(" ")[1][:5] # Estrae solo "18:00"
            temp = previsione['main']['temp']
            condizioni = previsione['weather'][0]['description'].capitalize()

            lista_previsioni.append({
                "ora": ora,
                "temp": temp,
                "condizioni": condizioni
            })
        return lista_previsioni
    return None

@st.cache_data(ttl=600)
def chiamata(city, temp, desc):
    prompt=f"Sei un pappagallo simpatico. A {city} ci sono {temp} gradi e il tempo è {desc}. Commenta brevemente il tempo"
    try:
        risposta=client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return risposta.text
    except Exception as e:
        # TENTATIVO B: Se Gemini fallisce (es. errore 429), usiamo Groq

        chat_completion = client_groq.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile", # Modello potentissimo e gratis
        )
        return chat_completion.choices[0].message.content

st.set_page_config(page_title="Meteo App", page_icon="🌤️")

st.title("🌦️Il meteo del pappagallo🦜", anchor=False)
st.write("Inserisci il nome di una città per sapere che tempo fa." )

citta = st.text_input("Città", placeholder="Es: Roma")

if st.button("Controlla Meteo") or citta:
    if not api_key:
        st.error("Errore: Chiave API non trovata!",anchor=False)
    elif citta:
        with st.status(f"Volando verso {citta}...", expanded=True) as status:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={citta}&appid={api_key}&units=metric&lang=it"
            res = requests.get(url)
            if res.status_code == 200:
                dati = res.json()
                temp = dati["main"]["temp"]
                desc = dati["weather"][0]["description"]
                st.markdown(f"### **{desc}**")
                st.write(f"🌡️ {temp}°C")

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


        previsioni = prendi_previsioni(citta, api_key)

        if previsioni and citta:
            st.title("🌦️ Previsioni Prossime Ore", anchor=False)
            # Creiamo 4 colonne per mostrare le ore fianco a fianco
            cols = st.columns(4)

            for i, p in enumerate(previsioni):
                with cols[i]:
                    st.caption(f"Ore {p['ora'][:2]}") # Testo piccolo per l'ora

                    # --- ENFASI SULLE CONDIZIONI ---
                    st.subheader(p['condizioni'], anchor=False)
                    st.write(f"🌡️ {p['temp']}°C")
        else:
            st.error("Non è stato possibile recuperare le informazioni nelle prossime ore")

    else:
        st.warning("Per favore, inserisci il nome di una città.")