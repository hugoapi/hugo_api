import streamlit as st
import pandas as pd
import os

url = https://raw.githubusercontent.com/hugoapi/hugo_api/main/data.csv

# Fonction pour lire le fichier CSV
def read_csv():
    return pd.read_csv(url)


# Fonction pour écrire dans le fichier CSV
def write_csv(dataframe, filepath="data.csv"):
    dataframe.to_csv(filepath, index=False)

# Obtenir le SHA du fichier actuel sur GitHub
def get_file_sha():
    url = "https://api.github.com/repos/hugoapi/hugo_api/contents/data.csv"
    headers = {
        'Authorization': 'token YOUR_GITHUB_TOKEN'
    }
    response = requests.get(url, headers=headers)
    return response.json()['sha']

# Mettre à jour le fichier sur GitHub
def update_github_file(filepath="data.csv", message="Update data.csv"):
    with open(filepath, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    
    sha = get_file_sha()
    
    url = "https://api.github.com/repos/hugoapi/hugo_api/contents/data.csv"
    payload = {
        "message": message,
        "committer": {
            "name": "Your Name",
            "email": "your-email@example.com"
        },
        "content": content,
        "sha": sha
    }
    headers = {
        'Authorization': 'token YOUR_GITHUB_TOKEN'
    }
    response = requests.put(url, json=payload, headers=headers)
    return response.json()

# Champs du formulaire
VOLUME = st.number_input("classroom volume", min_value=0, max_value=10000, step=1, value=int(0))
TOTAL_STUDENTS = st.number_input("Number of students", min_value=0, max_value=10000, step=1, value=int(0))
OCCUPIED_TIME = st.number_input("occupancy duration", min_value=0, max_value=10000, step=1,  value=int(0))
OPENING_WINDOW_TIME = st.number_input("Window opening duration", min_value=0, max_value=10000, step=1, value=int(0))
OPENING_SIZE_WINDOW = st.number_input("opening size window" , min_value=0, max_value=10000, step=1, value=int(0) )
OPENING_SIZE_DOOR = st.number_input("opening size door" , min_value=0, max_value=10000, step=1, value=int(0) )
OPENING_TIME_DOOR = st.number_input("opening time door" , min_value=0, max_value=10000, step=1, value=int(0) )


# Bouton pour soumettre le formulaire
if st.button("Soumettre"):
    if not VOLUME or not TOTAL_STUDENTS or not OCCUPIED_TIME or not OPENING_WINDOW_TIME:
        st.error("Veuillez remplir tous les champs.")
    else:
        df = read_csv()
        new_entry = pd.DataFrame({
            "Data": [f"{VOLUME},{TOTAL_STUDENTS},{OCCUPIED_TIME},{OPENING_SIZE_WINDOW},{OPENING_WINDOW_TIME},{OPENING_SIZE_DOOR},{OPENING_TIME_DOOR}"]
        })
        df = pd.concat([df, new_entry], ignore_index=True)
        write_csv(df)
