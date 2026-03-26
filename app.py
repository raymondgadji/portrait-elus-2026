"""
app.py  —  Portrait des Élus Municipaux 2026
Page d'accueil : KPIs globaux + présentation du projet
"""

import streamlit as st
from utils.loader import charger_maires, charger_conseillers

st.set_page_config(
    page_title="Portrait des Élus Municipaux 2026",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🗳️ Portrait des Élus Municipaux 2026")
st.markdown(
    """
    **Qui sont les élu·es qui nous gouvernent ?** Sont-ils représentatifs de la population française ?

    Ce tableau de bord explore les profils des **maires** et **conseillers municipaux** issus
    des élections des 15 et 22 mars 2026, à partir des données ouvertes du
    [Répertoire National des Élus](https://www.data.gouv.fr/datasets/repertoire-national-des-elus-1)
    (Ministère de l'Intérieur).

    ---
    📌 *Projet réalisé dans le cadre du [Challenge Open Data data.gouv.fr](https://defis.data.gouv.fr/defis/elections-municipales-2026-profils-des-elus)
    — Défi 2 : Profil des élu·es — mot-clé `defi-municipales-2026-résultats`*
    """
)

maires      = charger_maires()
conseillers = charger_conseillers()

total_elus        = len(maires) + len(conseillers)
pct_f_maires      = (maires["sexe"] == "F").mean() * 100
pct_f_conseillers = (conseillers["sexe"] == "F").mean() * 100
age_moy_maires    = maires["age"].dropna().mean()
age_moy_cons      = conseillers["age"].dropna().mean()

st.markdown("## 📊 Chiffres clés")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total élu·es analysé·es",
              f"{total_elus:,}".replace(",", " "))
with col2:
    st.metric("Femmes maires",
              f"{pct_f_maires:.1f} %",
              delta=f"soit {(maires['sexe']=='F').sum():,} maires".replace(",", " "),
              delta_color="off")
with col3:
    st.metric("Femmes conseillères",
              f"{pct_f_conseillers:.1f} %",
              delta=f"soit {(conseillers['sexe']=='F').sum():,} conseillères".replace(",", " "),
              delta_color="off")
with col4:
    st.metric("Âge moyen des maires",
              f"{age_moy_maires:.1f} ans",
              delta=f"conseillers : {age_moy_cons:.1f} ans",
              delta_color="off")

st.markdown("---")
st.markdown("## 🧭 Naviguer dans l'application")
st.markdown("*Cliquez sur un onglet dans la barre latérale gauche pour explorer chaque thématique.*")

col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.markdown("""
    **👥 Parité**
    - Répartition femmes/hommes
    - Par département
    - Comparaison vs population française
    """)
with col_b:
    st.markdown("""
    **🎂 Âge**
    - Distribution des âges
    - Par tranche et par genre
    - Âge moyen par département
    """)
with col_c:
    st.markdown("""
    **💼 Professions**
    - Grandes catégories CSP
    - Détail par profession
    - Comparaison vs population active
    """)
with col_d:
    st.markdown("""
    **🗺️ Carte**
    - Carte interactive France
    - % femmes, âge moyen, nb maires
    - Données par département
    """)

st.markdown("---")
st.caption(
    "Source : Répertoire National des Élus (RNE) — Ministère de l'Intérieur | "
    "Licence Ouverte / Open Licence 2.0 | Données : décembre 2025"
)