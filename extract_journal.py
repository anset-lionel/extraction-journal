import streamlit as st
import pandas as pd

# Application Streamlit
st.title('Extraction de Journal depuis Excel')

# Charger le fichier Excel
uploaded_file = st.file_uploader("Chargez votre fichier Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Vérifier si la colonne 'C' existe
    if len(df.columns) >= 3:
        journals = df.iloc[:, 2].dropna().unique()
        journal_selected = st.selectbox("Choisissez le journal à extraire", journals)

        if st.button('Extraire et télécharger en CSV'):
            filtered_df = df[df.iloc[:, 2] == journal_selected].copy()
            
            # Arrondi sans décimale pour toutes les colonnes numériques
            numeric_cols = filtered_df.select_dtypes(include=['number']).columns
            filtered_df[numeric_cols] = filtered_df[numeric_cols].round(0).astype(int)

            csv = filtered_df.to_csv(index=False, sep=';').encode('utf-8')

            st.download_button(
                label="Télécharger CSV",
                data=csv,
                file_name=f'journal_{journal_selected}.csv',
                mime='text/csv',
            )
    else:
        st.error("Le fichier ne contient pas suffisamment de colonnes pour réaliser cette opération.")
