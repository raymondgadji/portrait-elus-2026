"""
pages/2_Âge.py  —  Distribution des âges des élu·es municipaux
"""

import streamlit as st
import plotly.express as px
import pandas as pd

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
                Source : Répertoire National des Élus (RNE) — Ministère de l’Intérieur
                | Licence Ouverte 2.0 | Données : décembre 2025
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

from utils.loader import charger_maires, charger_conseillers

st.set_page_config(page_title="Âge des élus", page_icon="🎂", layout="wide")
st.title("🎂 Âge des élu·es")
st.markdown(
    "Quel est le profil générationnel des élu·es municipaux ? "
    "Les jeunes sont-ils représentés dans nos conseils municipaux ?"
)

maires      = charger_maires()
conseillers = charger_conseillers()

tab1, tab2, tab3 = st.tabs(["Distribution", "Par genre", "Par département"])

# ══════════════════════════════════════════════════════
# TAB 1 — Distribution globale
# ══════════════════════════════════════════════════════
with tab1:
    col_g, col_d = st.columns(2)

    with col_g:
        st.subheader("Maires")
        age_m = maires["age"].dropna()
        fig = px.histogram(
            age_m, nbins=40,
            labels={"value": "Âge", "count": "Nombre"},
            color_discrete_sequence=["#457b9d"],
            title=f"Distribution des âges — maires (moy. {age_m.mean():.1f} ans)",
        )
        fig.add_vline(x=age_m.mean(), line_dash="dash", line_color="red",
                      annotation_text=f"Moyenne : {age_m.mean():.1f} ans",
                      annotation_position="top right")
        st.plotly_chart(fig, use_container_width=True)

    with col_d:
        st.subheader("Conseillers municipaux")
        age_c = conseillers["age"].dropna()
        fig2 = px.histogram(
            age_c, nbins=40,
            labels={"value": "Âge", "count": "Nombre"},
            color_discrete_sequence=["#2a9d8f"],
            title=f"Distribution des âges — conseillers (moy. {age_c.mean():.1f} ans)",
        )
        fig2.add_vline(x=age_c.mean(), line_dash="dash", line_color="red",
                       annotation_text=f"Moyenne : {age_c.mean():.1f} ans",
                       annotation_position="top right")
        st.plotly_chart(fig2, use_container_width=True)

    # Tranches d'âge
    st.markdown("### Répartition par tranche d'âge")

    tranches_m = maires["tranche_age"].value_counts().sort_index().reset_index()
    tranches_m.columns = ["Tranche", "Nombre"]
    tranches_m["Pct"] = (tranches_m["Nombre"] / tranches_m["Nombre"].sum() * 100).round(1)
    tranches_m["Type"] = "Maires"

    tranches_c = conseillers["tranche_age"].value_counts().sort_index().reset_index()
    tranches_c.columns = ["Tranche", "Nombre"]
    tranches_c["Pct"] = (tranches_c["Nombre"] / tranches_c["Nombre"].sum() * 100).round(1)
    tranches_c["Type"] = "Conseillers"

    df_tranches = pd.concat([tranches_m, tranches_c])
    df_tranches["Tranche"] = df_tranches["Tranche"].astype(str)

    fig_t = px.bar(
        df_tranches, x="Tranche", y="Pct", color="Type", barmode="group",
        color_discrete_map={"Maires": "#457b9d", "Conseillers": "#2a9d8f"},
        labels={"Pct": "% des élus", "Tranche": "Tranche d'âge"},
        title="Répartition par tranche d'âge : maires vs conseillers",
        text="Pct",
    )
    fig_t.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig_t, use_container_width=True)

    # ── Statistiques avec phrases complètes ───────────────────────────────
    st.markdown("### Statistiques")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Âge moyen maires",       f"{age_m.mean():.1f} ans")
    col2.metric("Âge médian maires",      f"{age_m.median():.0f} ans")
    col3.metric("Âge moyen conseillers",  f"{age_c.mean():.1f} ans")
    col4.metric("Âge médian conseillers", f"{age_c.median():.0f} ans")

    pct_moins30_m = (maires["age"] < 30).mean() * 100
    pct_moins30_c = (conseillers["age"] < 30).mean() * 100
    pct_plus70_m  = (maires["age"] >= 70).mean() * 100
    nb_moins30_m  = (maires["age"] < 30).sum()
    nb_moins30_c  = (conseillers["age"] < 30).sum()

    st.info(
        f"**Les jeunes sont quasi absents des mandats :** seulement **{pct_moins30_m:.1f}%** des maires "
        f"({nb_moins30_m:,} personnes) ont moins de 30 ans, contre **{pct_moins30_c:.1f}%** "
        f"({nb_moins30_c:,} personnes) parmi les conseillers municipaux. "
        f"À l'inverse, **{pct_plus70_m:.1f}%** des maires ont 70 ans ou plus."
        .replace(",", " ")
    )

# ══════════════════════════════════════════════════════
# TAB 2 — Par genre
# ══════════════════════════════════════════════════════
with tab2:
    st.subheader("Âge des maires selon le genre")

    fig_box = px.box(
        maires.dropna(subset=["age"]),
        x="sexe", y="age",
        color="sexe",
        color_discrete_map={"M": "#457b9d", "F": "#e76f51"},
        labels={"sexe": "Genre", "age": "Âge"},
        category_orders={"sexe": ["F", "M"]},
        title="Distribution des âges par genre — maires",
        points="outliers",
    )
    fig_box.update_xaxes(ticktext=["Femmes", "Hommes"], tickvals=["F", "M"])
    st.plotly_chart(fig_box, use_container_width=True)

    age_f = maires[maires["sexe"] == "F"]["age"].dropna()
    age_h = maires[maires["sexe"] == "M"]["age"].dropna()
    c1, c2 = st.columns(2)
    c1.metric("Âge moyen — Femmes maires", f"{age_f.mean():.1f} ans")
    c2.metric("Âge moyen — Hommes maires", f"{age_h.mean():.1f} ans")

    diff = age_h.mean() - age_f.mean()
    if diff > 0:
        st.markdown(
            f"Les femmes maires sont en moyenne **{diff:.1f} ans plus jeunes** que leurs homologues masculins "
            f"({age_f.mean():.1f} ans vs {age_h.mean():.1f} ans)."
        )
    else:
        st.markdown(
            f"Les femmes maires sont en moyenne **{abs(diff):.1f} ans plus âgées** que leurs homologues masculins "
            f"({age_f.mean():.1f} ans vs {age_h.mean():.1f} ans)."
        )

# ══════════════════════════════════════════════════════
# TAB 3 — Par département
# ══════════════════════════════════════════════════════
with tab3:
    st.subheader("Âge moyen des maires par département")

    age_dep = (
        maires.groupby("dep")["age"]
        .mean()
        .reset_index()
        .rename(columns={"age": "age_moyen"})
        .sort_values("age_moyen")
    )
    age_dep["age_moyen"] = age_dep["age_moyen"].round(1)

    dep_min = age_dep.iloc[0]
    dep_max = age_dep.iloc[-1]

    fig_dep = px.bar(
        age_dep, x="age_moyen", y="dep", orientation="h",
        color="age_moyen",
        color_continuous_scale="RdYlGn_r",
        labels={"age_moyen": "Âge moyen", "dep": "Département"},
        title="Âge moyen des maires par département",
        height=1600,
    )
    fig_dep.add_vline(x=age_dep["age_moyen"].mean(), line_dash="dash", line_color="blue",
                      annotation_text="Moyenne nationale",
                      annotation_position="top right")
    fig_dep.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_dep, use_container_width=True)

    st.markdown(
        f"**{dep_min['dep']}** est le département avec les maires les plus jeunes en moyenne "
        f"(**{dep_min['age_moyen']} ans**), tandis que **{dep_max['dep']}** affiche la moyenne "
        f"la plus élevée (**{dep_max['age_moyen']} ans**)."
    )

afficher_footer()