import streamlit as st
import pandas as pd
import os


# Fonction pour lire le fichier CSV
def read_csv():
        return pd.read_csv("https://raw.githubusercontent.com/hugoapi/hugo_api/main/data.csv")


# Fonction pour écrire dans le fichier CSV
def write_csv(dataframe):
    dataframe.to_csv("https://raw.githubusercontent.com/hugoapi/hugo_api/main/data.csv", index=False)


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
