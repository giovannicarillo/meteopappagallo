import requests
import os
from dotenv import load_dotenv

# 1. Carica le variabili nascoste nel file .env
load_dotenv()
CHIAVE_API = os.getenv("API_KEY")

def chiedi_meteo(citta):
    # 2. Costruiamo l'URL per chiamare il server di OpenWeatherMap
    # Usiamo il sistema metrico per avere i gradi Celsius
    url = f"http://api.openweathermap.org/data/2.5/weather?q={citta}&appid={CHIAVE_API}&units=metric&lang=it"

    # 3. Facciamo la richiesta (come se stessimo aprendo la pagina web)
    risposta = requests.get(url)

    # 4. Controlliamo se è andata a buon fine (Codice 200 = Tutto OK)
    if risposta.status_code == 200:
        # Convertiamo la risposta in un dizionario Python (JSON)
        dati = risposta.json()

        # Estraiamo solo i dati che ci interessano navigando nel dizionario
        temperatura = dati["main"]["temp"]
        descrizione = dati["weather"][0]["description"]

        print(f"\n🌍 Meteo a {citta.capitalize()}:")
        print(f"🌡️ Temperatura: {temperatura}°C")
        print(f"☁️ Condizioni: {descrizione}\n")
    else:
        print("❌ Errore: Città non trovata o problema di connessione.")

# 5. Facciamo partire il programma
if __name__ == "__main__":
    print("--- BENVENUTO NEL PAPPAGALLO METEO ---")
    citta_utente = input("Di quale città vuoi sapere il meteo? ")
    chiedi_meteo(citta_utente)