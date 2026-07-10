import sys
import os
import requests
import streamlit as st
import pandas as pd
import numpy as np

# 1. Gestion des chemins Python et imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.logger import logger

# 2. Configuration visuelle de la page
st.set_page_config(page_title="Salary Dashboard & Prediction", page_icon="💰", layout="wide")

# Injection CSS pour améliorer l'expérience utilisateur (curseur pointer)
st.markdown(
    """
    <style>
    div[data-testid="stSelectbox"] div { cursor: pointer !important; }
    div[data-testid="stButton"] button { cursor: pointer !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Chargement des données simulées pour la partie Analytics (Haut de page)
@st.cache_data
def load_analytics_data():
    np.random.seed(42)
    n_samples = 200
    ages = np.random.randint(22, 60, n_samples)
    experiences = np.random.randint(1, 35, n_samples)
    departments = np.random.choice(["Finance", "IT", "RH"], n_samples)
    salaries = 150000 + (experiences * 25000) + (ages * 2000) + np.random.randint(-50000, 50000, n_samples)
    
    return pd.DataFrame({
        "age": ages,
        "experience": experiences,
        "department": departments,
        "salary": salaries
    })

df = load_analytics_data()

# --- TITRE DE L'APPLICATION ---
st.title("📊 Salary Management & Prediction Dashboard")
st.write("Consultez les statistiques de l'entreprise et simulez de nouvelles prédictions budgétaires.")
st.markdown("---")

# --- SECTION 1 : ANALYTICS & GRAPH_CHARTS ---
st.subheader("📈 Analyses globales de l'entreprise")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Nombre d'employés analysés", value=f"{len(df)}")
with col2:
    st.metric(label="Salaire Moyen Global", value=f"{df['salary'].mean():,.0f} FCFA")
with col3:
    st.metric(label="Salaire Maximum constaté", value=f"{df['salary'].max():,.0f} FCFA")

st.write("") 

graph_col1, graph_col2 = st.columns(2)
with graph_col1:
    st.markdown("#### 🏢 Moyenne des salaires par Département")
    df_dept = df.groupby("department")["salary"].mean().reset_index()
    # Syntaxe mise à jour : width="stretch" au lieu de use_container_width=True
    st.bar_chart(data=df_dept, x="department", y="salary", width="stretch")

with graph_col2:
    st.markdown("#### ⏳ Évolution du salaire selon l'expérience")
    # Syntaxe mise à jour : width="stretch" au lieu de use_container_width=True
    st.scatter_chart(data=df, x="experience", y="salary", color="department", width="stretch")

st.markdown("---")

# --- SECTION 2 : FORMULAIRE DE PRÉDICTION ---
st.subheader("🔮 Calculateur de Salaire (IA Model Inférence)")

form_col1, form_col2, form_col3 = st.columns(3)
with form_col1:
    age = st.number_input("Âge", min_value=18, max_value=65, value=30)
with form_col2:
    experience = st.number_input("Expérience (en années)", min_value=0, max_value=40, value=5)
with form_col3:
    department = st.selectbox("Département", ["Finance", "IT", "RH"])

st.write("")

if st.button("Prédire le salaire", type="primary", use_container_width=True):
    logger.info("Nouvelle demande utilisateur initiée pour la prédiction.")

    finance = 1 if department == "Finance" else 0
    it = 1 if department == "IT" else 0
    rh = 1 if department == "RH" else 0

    data = {
        "age": age,
        "experience": experience,
        "finance": finance,
        "it": it,
        "rh": rh,
    }

    url_prediction = "http://127.0.0.1:8000/predict"

    try:
        response = requests.post(url_prediction, json=data, timeout=10)
        response.raise_for_status()
        
        salary = response.json()["predicted_salary"]
        logger.info("Réponse reçue avec succès depuis FastAPI.")

        st.success(f"### **Résultat de la simulation : {salary:,.0f} FCFA**")
        st.balloons()
        
    except Exception as e:
        logger.error(f"Erreur d'exécution : {e}")
        st.error(f"🚨 Erreur lors du calcul : {e}")

st.markdown("---")

# --- SECTION 3 : HISTORIQUE DES PRÉDICTIONS (VIA FASTAPI GET) ---
st.subheader("📜 Historique des dernières simulations en temps réel")

url_historique = "http://127.0.0.1:8000/predictions?limit=5"

try:
    # Streamlit interroge proprement FastAPI au lieu d'attaquer la BDD en direct
    response_hist = requests.get(url_historique, timeout=5)
    
    if response_hist.status_code == 200:
        predictions_json = response_hist.json()
        
        if predictions_json:  # Si la liste contient des enregistrements
            df_history = pd.DataFrame(predictions_json)
            # Syntaxe mise à jour : width="stretch" au lieu de use_container_width=True
            st.dataframe(
                df_history, 
                width="stretch", 
                hide_index=True
            )
        else:
            st.info("L'historique est actuellement vide en base de données. Effectuez une prédiction !")
    else:
        st.warning("⚠️ L'API a refusé de renvoyer l'historique.")
        
except Exception as e:
    logger.error(f"Impossible de joindre l'endpoint d'historique : {e}")
    st.warning("⚠️ Impossible de charger l'historique depuis l'API FastAPI.")