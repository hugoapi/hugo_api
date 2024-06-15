import streamlit as st
import os

github_token = os.getenv('GITHUB_TOKEN')
st.write(f"Token récupéré : {github_token}")
