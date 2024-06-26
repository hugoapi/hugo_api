import streamlit as st
import pandas as pd
import base64
import requests
import os

# Récupérer le token d'accès personnel depuis les variables d'environnement
github_token = os.getenv('GITHUB_TOKEN')
if github_token:
    st.write("Token récupéré avec succès.")  # Message de débogage
else:
    st.error("Le token GitHub n'a pas été trouvé. Veuillez définir la variable d'environnement GITHUB_TOKEN.")
    raise ValueError("GitHub token is missing.")

# Lire le fichier CSV depuis GitHub
def read_csv():
    try:
        url = "https://raw.githubusercontent.com/hugoapi/hugo_api/main/database.csv"
        st.write(f"Lecture du fichier CSV depuis l'URL : {url}")  # Message de débogage
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier CSV : {e}")
        return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur

# Écrire localement dans le fichier CSV
def write_csv(dataframe, filepath="database.csv"):
    try:
        dataframe.to_csv(filepath, index=False)
        st.write(f"Fichier CSV écrit localement à : {filepath}")  # Message de débogage
    except Exception as e:
        st.error(f"Erreur lors de l'écriture du fichier CSV : {e}")

# Obtenir le SHA du fichier actuel sur GitHub
def get_file_sha():
    try:
        url = "https://api.github.com/repos/hugoapi/hugo_api/contents/database.csv"
        headers = {
            'Authorization': f'token {github_token}'  
        }
        st.write(f"Envoi de la requête GET pour obtenir le SHA du fichier depuis l'URL : {url}")  # Message de débogage
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        sha = response.json()['sha']
        st.write(f"SHA récupéré : {sha}")  # Message de débogage
        return sha
    except Exception as e:
        st.error(f"Erreur lors de la récupération du SHA du fichier : {e}")
        st.error(f"Response content: {response.content}")
        return None

# Mettre à jour le fichier sur GitHub
def update_github_file(filepath="database.csv", message="Update data.csv"):
    try:
        with open(filepath, "rb") as f:
            content = base64.b64encode(f.read()).decode()
            st.write("Fichier encodé en base64.")  # Message de débogage

        sha = get_file_sha()
        if sha is None:
            st.error("SHA du fichier introuvable. Mise à jour annulée.")
            return

        url = "https://api.github.com/repos/hugoapi/hugo_api/contents/database.csv"
        payload = {
            "message": message,
            "committer": {
                "name": "hugo",  
                "email": "hugobaugnies2000@gmail.com"  
            },
            "content": content,
            "sha": sha
        }
        headers = {
            'Authorization': f'token {github_token}' 
        }
        st.write(f"Envoi de la requête PUT pour mettre à jour le fichier à l'URL : {url}")  # Message de débogage
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()
        st.success("Le fichier sur GitHub a été mis à jour avec succès.")
    except Exception as e:
        st.error(f"Erreur lors de la mise à jour du fichier sur GitHub : {e}")

# Champs du formulaire
VOLUME = st.number_input("classroom volume", min_value=0, max_value=10000, step=1, value=int(0))
TOTAL_STUDENTS = st.number_input("Number of students", min_value=0, max_value=10000, step=1, value=int(0))
OCCUPIED_TIME = st.number_input("occupancy duration", min_value=0, max_value=10000, step=1, value=int(0))
OPENING_WINDOW_TIME = st.number_input("Window opening duration", min_value=0, max_value=10000, step=1, value=int(0))
OPENING_SIZE_WINDOW = st.number_input("opening size window", min_value=0, max_value=10000, step=1, value=int(0))
OPENING_SIZE_DOOR = st.number_input("opening size door", min_value=0, max_value=10000, step=1, value=int(0))
OPENING_TIME_DOOR = st.number_input("opening time door", min_value=0, max_value=10000, step=1, value=int(0))

# Bouton pour soumettre le formulaire
if st.button("Soumettre"):
    if not VOLUME or not TOTAL_STUDENTS or not OCCUPIED_TIME or not OPENING_WINDOW_TIME:
        st.error("Veuillez remplir tous les champs.")
    else:
        df = read_csv()
        if df.empty:
            st.error("Le fichier CSV n'a pas pu être lu. Soumission annulée.")
        else:
            new_entry = pd.DataFrame({
                "Data": [f"{VOLUME},{TOTAL_STUDENTS},{OCCUPIED_TIME},{OPENING_SIZE_WINDOW},{OPENING_WINDOW_TIME},{OPENING_SIZE_DOOR},{OPENING_TIME_DOOR}"]
            })
            df = pd.concat([df, new_entry], ignore_index=True)
            write_csv(df)
            update_github_file(message="Updating data.csv with new entry")
            st.success("Les données ont été soumises et enregistrées avec succès.")



