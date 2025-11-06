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
        'Player Name',
        'Session Date',
        'Time In Heart Rate Zone 5 (Relative)',
        'Time In Heart Rate Zone 6 (Relative)'
    }

    if not required_cols.issubset(df.columns):
        st.error(f"⚠️ Le fichier doit contenir les colonnes suivantes : {required_cols}")
    else:
        # Conversion des dates
        df['Session Date'] = pd.to_datetime(df['Session Date'], errors='coerce')

        # Calcul du temps total >90% FCmax (zones 5 + 6)
        df['Time_above_90_FCmax'] = (
            df['Time In Heart Rate Zone 5 (Relative)'].fillna(0) +
            df['Time In Heart Rate Zone 6 (Relative)'].fillna(0)
        )

        # Ajoute la semaine ISO
        df['Semaine'] = df['Session Date'].dt.isocalendar().week

        # === Résumé hebdomadaire par joueur ===
        weekly_summary = (
            df.groupby(['Player Name', 'Semaine'])['Time_above_90_FCmax']
            .sum()
            .reset_index()
            .rename(columns={'Time_above_90_FCmax': 'Temps total (>90% FCmax)'})
        )

        # === Résumé quotidien par joueur ===
        daily_summary = (
            df.groupby(['Player Name', 'Session Date'])['Time_above_90_FCmax']
            .sum()
            .reset_index()
            .rename(columns={'Time_above_90_FCmax': 'Temps total (>90% F_
