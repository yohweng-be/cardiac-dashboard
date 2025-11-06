import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Dashboard Cardiac", layout="wide")

st.title("🏋️ Dashboard Cardiac — Temps >90% FCmax")

# === Upload du CSV ===
uploaded_file = st.file_uploader("📤 Importer un fichier CSV", type=["csv"])

if uploaded_file:
    # Lecture du CSV
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    # Vérifie les colonnes nécessaires
    required_cols = {
        'Player',
        'Date',
        'Time In Heart Rate Zone 5 (Relative)',
        'Time In Heart Rate Zone 6 (Relative)'
    }
    if not required_cols.issubset(df.columns):
        st.error(f"⚠️ Le fichier doit contenir les colonnes suivantes : {required_cols}")
    else:
        # Conversion des dates
