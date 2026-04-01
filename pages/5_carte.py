"""
pages/4_Carte.py
----------------
Carte choroplèthe interactive par département
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from utils.loader import charger_maires, charger_conseillers

LINKEDIN = "https://www.linkedin.com/in/raymond-gadji/"

def afficher_footer():
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align:center; padding:0.8rem 0 0.2rem 0;">
            <p style="margin:0; font-size:0.85rem;">
                © 2026 Créé par
                <a href="{LINKEDIN}" target="_blank"
                   style="color:#4A90D9; text-decoration:none; font-weight:600;">
                    Raymond Gadji
                </a>
                — Data Analyst
            </p>
            <p style="margin:0.25rem 0 0 0; font-size:0.75rem; color:#888;">
                Source : Répertoire National des Élus (RNE) — Ministère de l'Intérieur
                | Licence Ouverte 2.0 | Données : décembre 2025
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

@st.cache_data(show_spinner="Chargement de la carte...")
def charger_geojson():
    url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson"
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception:
        return None

st.set_page_config(page_title="Carte", page_icon="🗺️", layout="wide")
st.title("🗺️ Carte interactive par département")
st.markdown("Explore la répartition des élu·es sur le territoire français.")

maires      = charger_maires()
conseillers = charger_conseillers()

# ── Indicateur à afficher ─────────────────────────────────────────────────
indicateur = st.selectbox(
    "Choisir l'indicateur à cartographier :",
    options=[
        "IRD — Indice de Représentativité Démocratique",
        "% de femmes maires",
        "Âge moyen des maires",
        "Nombre de maires",
    ]
)

# ── Calcul par département ────────────────────────────────────────────────
dep_stats = maires.groupby(["code_dep", "dep"]).agg(
    nb_maires  =("sexe", "count"),
    pct_femmes =("sexe", lambda x: round((x == "F").mean() * 100, 1)),
    age_moyen  =("age",  lambda x: round(x.mean(), 1)),
).reset_index()

def pct_cadres_dep(df):
    total = len(df)
    if total == 0:
        return 0
    cadres = df["csp"].str.lower().str.contains(
        "cadre|ingénieur|profession libérale|médecin|pharmacien|architecte|avocat",
        na=False
    ).sum()
    return cadres / total * 100

csp_dep = maires.groupby("code_dep").apply(pct_cadres_dep).reset_index()
csp_dep.columns = ["code_dep", "pct_cadres"]
dep_stats = dep_stats.merge(csp_dep, on="code_dep", how="left")

ecart_genre = (dep_stats["pct_femmes"] - 51.6).abs()
score_genre = (100 - ecart_genre.clip(0, 100)).clip(0, 100)

ecart_age   = (dep_stats["age_moyen"] - 42.0).abs()
score_age   = (100 - (ecart_age / 30 * 100)).clip(0, 100)

ecart_csp   = (dep_stats["pct_cadres"] - 18.0).abs()
score_csp   = (100 - ecart_csp.clip(0, 100)).clip(0, 100)

dep_stats["ird_dep"] = (
    score_genre * 0.40 +
    score_age   * 0.35 +
    score_csp   * 0.25
).round(1)

if indicateur == "IRD — Indice de Représentativité Démocratique":
    col_val = "ird_dep"
    titre   = "IRD moyen par département — Indice de Représentativité Démocratique"
    palette = ["#e76f51", "#e9c46a", "#2a9d8f"]
elif indicateur == "% de femmes maires":
    col_val = "pct_femmes"
    titre   = "% de femmes maires par département"
    palette = "RdBu"
elif indicateur == "Âge moyen des maires":
    col_val = "age_moyen"
    titre   = "Âge moyen des maires par département"
    palette = "RdYlGn_r"
else:
    col_val = "nb_maires"
    titre   = "Nombre de maires par département"
    palette = "Blues"

# ── GeoJSON départements France ───────────────────────────────────────────
geojson = charger_geojson()

if geojson is None:
    st.warning(
        "Impossible de charger les contours des départements (connexion réseau requise). "
        "Affichage en tableau à la place."
    )
    st.dataframe(
        dep_stats[["dep", "code_dep", col_val]].sort_values(col_val, ascending=False),
        use_container_width=True,
        hide_index=True,
    )
else:
    fig_map = px.choropleth(
        dep_stats,
        geojson=geojson,
        locations="code_dep",
        featureidkey="properties.code",
        color=col_val,
        hover_name="dep",
        hover_data={
            "pct_femmes": True,
            "age_moyen" : True,
            "nb_maires" : True,
            "ird_dep"   : True,
            "code_dep"  : False,
        },
        color_continuous_scale=palette,
        title=titre,
        labels={
            "pct_femmes": "% femmes",
            "age_moyen" : "Âge moyen",
            "nb_maires" : "Nb maires",
            "ird_dep"   : "IRD",
        },
    )
    fig_map.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
    )
    fig_map.update_layout(
        height=650,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
    )
    st.plotly_chart(fig_map, use_container_width=True)

# ── Tableau récapitulatif ─────────────────────────────────────────────────
with st.expander("📋 Voir les données complètes par département"):
    st.dataframe(
        dep_stats.rename(columns={
            "dep"       : "Département",
            "code_dep"  : "Code",
            "nb_maires" : "Nb maires",
            "pct_femmes": "% femmes",
            "age_moyen" : "Âge moyen",
            "ird_dep"   : "IRD",
        }).sort_values("Département"),
        use_container_width=True,
        hide_index=True,
    )

afficher_footer()