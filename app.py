import streamlit as st
import requests
import os

from pathlib import Path
from dotenv import load_dotenv

# Chemin vers .env_api
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env_api")

# Récupération des clés
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


API_URL = 'http://localhost:8000/api/'

# -------------------- FONCTIONS --------------------

def get_address_suggestions(input_text):
    """Récupère les suggestions d'adresses à partir du texte saisi"""
    if not input_text:
        return []

    url = (
        "https://maps.googleapis.com/maps/api/place/autocomplete/json"
        f"?input={input_text}"
        f"&key={GOOGLE_API_KEY}"
        "&types=geocode"
        "&language=fr"
    )
    response = requests.get(url).json()
    if response["status"] == "OK":
        return [ {"description": pred["description"], "place_id": pred["place_id"]}
            for pred in response["predictions"] ]
    return []

def find_place_id(description, suggestions):
    """Trouve le place_id à partir de la description sélectionnée"""
    for s in suggestions:
        if s["description"] == description:
            return s["place_id"]
    return None

def get_estimation(data: dict):
    url = f'{API_URL}estimation/'
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    return None

def start_course(data: dict):
    url = f"{API_URL}start_course/"
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    return None

def get_course_history():
    url = f"{API_URL}course_history/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

# -------------------- SESSION --------------------

if 'estimation_ready' not in st.session_state:
    st.session_state.estimation_ready = False

# -------------------- INTERFACE --------------------

st.title("🛵 Estimation de course")

# Adresse de départ
st.subheader("Adresse de départ")
input_departure = st.text_input("Entrez l'adresse de départ")
departure_suggestions = get_address_suggestions(input_departure) if input_departure else []
departure_options = [s["description"] for s in departure_suggestions]
selected_departure = st.selectbox("Suggestions de départ :", departure_options)

# Adresse d’arrivée
st.subheader("Adresse d’arrivée")
input_arrival = st.text_input("Entrez l'adresse d’arrivée")
arrival_suggestions = get_address_suggestions(input_arrival) if input_arrival else []
arrival_options = [s["description"] for s in arrival_suggestions]
selected_arrival = st.selectbox("Suggestions d’arrivée :", arrival_options)

# Estimation
if st.button("🎯 Estimer le prix"):
    departure_place_id = find_place_id(selected_departure, departure_suggestions)
    arrival_place_id = find_place_id(selected_arrival, arrival_suggestions)
    st.write(f"Nos ID : {departure_place_id}, {arrival_place_id}")

    if departure_place_id and arrival_place_id:
        estimation = get_estimation({
            "departure_place_id": departure_place_id,
            "arrival_place_id": arrival_place_id
        })


        if estimation:
            st.session_state.estimation = estimation
            st.session_state.estimation_ready = True

            st.success(f"💰 Prix estimé : {estimation['estimated_price']} CAD")
            st.info(f"⏱ Temps estimé : {round(estimation['estimated_time'], 1)} minutes")
            st.write(f"🚦 Trafic : {estimation['traffic']}")
            st.write(f"🌤️ Météo : {estimation['weather']}")
        else:
            st.error("Erreur lors de l’estimation.")
    else:
        st.warning("Sélectionnez une adresse valide pour les deux champs.")

# Commencer la course
if st.session_state.estimation_ready:
    if st.button("🚗 Commencer la course"):
        data_to_save = st.session_state.estimation.copy()
        data_to_save["departure_address"] = selected_departure
        data_to_save["arrival_address"] = selected_arrival
        data_to_save["user"] = 1  # En dur pour l’instant
        response = start_course(data_to_save)
        if response:
            st.success("✅ Course enregistrée avec succès !")
        else:
            st.error("Erreur lors de l’enregistrement de la course.")

# Historique
if st.button("📜 Voir l'historique des courses"):
    history = get_course_history()
    if isinstance(history, list) and len(history) > 0:
        st.write("### Historique des courses :")
        for i, course in enumerate(history):
            st.markdown(f"""
            **Course {i + 1}**  
            - 🏁 Départ : `{course['departure_address']}`  
            - 🎯 Arrivée : `{course['arrival_address']}`  
            - 📏 Distance : `{round(course['distance_km'], 2)} km`  
            - ⏱ Temps estimé : `{round(course['estimated_time'], 0)} minutes`  
            - 💰 Prix : `{course['estimated_price']} CAD`  
            ---
            """)
    else:
        st.info("Aucune course enregistrée.")
