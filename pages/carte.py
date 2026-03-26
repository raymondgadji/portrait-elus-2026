"""
pages/4_Carte.py
----------------
Carte choroplèthe interactive par département
"""

import streamlit as st
import plotly.express as px
import pandas as pd
import requests
from utils.loader import charger_maires

st.set_page_config(page_title="Carte", page_icon="🗺️", layout="wide")
st.title("🗺️ Carte interactive par département")
st.markdown("Explore la répartition des élu·es sur le territoire français.")

maires = charger_maires()

# ── Indicateur à afficher ─────────────────────────────────────────────────
indicateur = st.selectbox(
    "Choisir l'indicateur à cartographier :",
    options=[
        "% de femmes maires",
        "Âge moyen des maires",
        "Nombre de maires",
    ]
)

# ── Calcul par département ────────────────────────────────────────────────
dep_stats = maires.groupby(["code_dep", "dep"]).agg(
    nb_maires   =("sexe", "count"),
    pct_femmes  =("sexe", lambda x: round((x == "F").mean() * 100, 1)),
    age_moyen   =("age", lambda x: round(x.mean(), 1)),
).reset_index()

if indicateur == "% de femmes maires":
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

# ── GeoJSON départements France (source publique) ─────────────────────────
@st.cache_data(show_spinner="Chargement de la carte...")
def charger_geojson():
    url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson"
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception:
        return None

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
        hover_data={"pct_femmes": True, "age_moyen": True, "nb_maires": True, "code_dep": False},
        color_continuous_scale=palette,
        title=titre,
        labels={
            "pct_femmes" : "% femmes",
            "age_moyen"  : "Âge moyen",
            "nb_maires"  : "Nb maires",
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
        }).sort_values("Département"),
        use_container_width=True,
        hide_index=True,
    )

st.markdown("---")
st.caption("Source : RNE — Ministère de l'Intérieur | GeoJSON : gregoiredavid/france-geojson | Licence Ouverte 2.0")