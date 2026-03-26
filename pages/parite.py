"""
pages/1_Parité.py  —  Analyse de la parité hommes / femmes
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.loader import charger_maires, charger_conseillers

st.set_page_config(page_title="Parité", page_icon="👥", layout="wide")
st.title("👥 Parité hommes / femmes")
st.markdown(
    "La loi sur la parité oblige les listes à alterner femmes et hommes pour les communes "
    "de plus de 1 000 habitants. Les maires, eux, sont élus librement. Qu'en est-il en pratique ?"
)

maires      = charger_maires()
conseillers = charger_conseillers()

tab1, tab2, tab3 = st.tabs(["Vue globale", "Par département", "Classements"])

# ══════════════════════════════════════════════════════
# TAB 1 — Vue globale
# ══════════════════════════════════════════════════════
with tab1:
    col_g, col_d = st.columns(2)

    with col_g:
        st.subheader("Maires")
        counts_m = maires["sexe"].value_counts().reset_index()
        counts_m.columns = ["Sexe", "Nombre"]
        counts_m["Sexe"] = counts_m["Sexe"].map({"M": "Hommes", "F": "Femmes"})
        fig_m = px.pie(
            counts_m, names="Sexe", values="Nombre",
            color="Sexe",
            color_discrete_map={"Femmes": "#e76f51", "Hommes": "#457b9d"},
            hole=0.45,
            title=f"{len(maires):,} maires — {(maires['sexe']=='F').mean()*100:.1f}% de femmes".replace(",", " "),
        )
        fig_m.update_traces(textinfo="percent+label", textfont_size=14)
        st.plotly_chart(fig_m, use_container_width=True)

    with col_d:
        st.subheader("Conseillers municipaux")
        counts_c = conseillers["sexe"].value_counts().reset_index()
        counts_c.columns = ["Sexe", "Nombre"]
        counts_c["Sexe"] = counts_c["Sexe"].map({"M": "Hommes", "F": "Femmes"})
        fig_c = px.pie(
            counts_c, names="Sexe", values="Nombre",
            color="Sexe",
            color_discrete_map={"Femmes": "#e76f51", "Hommes": "#457b9d"},
            hole=0.45,
            title=f"{len(conseillers):,} conseillers — {(conseillers['sexe']=='F').mean()*100:.1f}% de femmes".replace(",", " "),
        )
        fig_c.update_traces(textinfo="percent+label", textfont_size=14)
        st.plotly_chart(fig_c, use_container_width=True)

    # ── Comparaison avec la population ────────────────────────────────────
    pct_pop_f = 51.6
    pct_f_m   = (maires["sexe"] == "F").mean() * 100
    pct_f_c   = (conseillers["sexe"] == "F").mean() * 100
    ecart_m   = pct_f_m - pct_pop_f
    ecart_c   = pct_f_c - pct_pop_f

    st.markdown("---")
    st.markdown("### Comparaison avec la population française")

    col1, col2, col3 = st.columns(3)
    col1.metric("Femmes dans la population (INSEE)", f"{pct_pop_f:.1f} %")
    col2.metric("Femmes maires",       f"{pct_f_m:.1f} %",
                delta=f"{ecart_m:.1f} pts", delta_color="inverse")
    col3.metric("Femmes conseillères", f"{pct_f_c:.1f} %",
                delta=f"{ecart_c:.1f} pts", delta_color="inverse")

    # Phrases explicatives claires
    st.markdown(f"""
    **Ce que signifient ces chiffres :**

    - Les femmes représentent **{pct_pop_f:.1f}%** de la population française (source INSEE).
    - Parmi les **maires**, elles ne sont que **{pct_f_m:.1f}%** :
      c'est **{abs(ecart_m):.1f} points de pourcentage en dessous** de leur part dans la population.
      Autrement dit, les femmes sont très largement sous-représentées à la tête des mairies.
    - Parmi les **conseillers municipaux**, elles atteignent **{pct_f_c:.1f}%** :
      c'est encore **{abs(ecart_c):.1f} points en dessous** de la parité réelle,
      mais la loi sur l'alternance des listes a nettement amélioré leur présence dans les conseils.
    """)

# ══════════════════════════════════════════════════════
# TAB 2 — Par département
# ══════════════════════════════════════════════════════
with tab2:
    st.subheader("Taux de femmes maires par département")

    dep_parite = (
        maires.groupby("dep")["sexe"]
        .apply(lambda x: (x == "F").mean() * 100)
        .reset_index()
        .rename(columns={"sexe": "pct_femmes"})
        .sort_values("pct_femmes", ascending=True)
    )
    dep_parite["pct_femmes"] = dep_parite["pct_femmes"].round(1)

    fig_dep = px.bar(
        dep_parite,
        x="pct_femmes", y="dep", orientation="h",
        color="pct_femmes",
        color_continuous_scale=["#457b9d", "#e76f51"],
        labels={"pct_femmes": "% de femmes maires", "dep": "Département"},
        title="% de femmes parmi les maires — par département",
        height=1600,
    )
    fig_dep.add_vline(x=50, line_dash="dash", line_color="gray",
                      annotation_text="50 %", annotation_position="top right")
    fig_dep.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig_dep, use_container_width=True)

    dep_min = dep_parite.iloc[0]
    dep_max = dep_parite.iloc[-1]
    moy_nat = dep_parite["pct_femmes"].mean()
    st.markdown(
        f"La moyenne nationale est de **{moy_nat:.1f}%** de femmes maires. "
        f"**{dep_max['dep']}** est le département le plus paritaire avec **{dep_max['pct_femmes']}%** de femmes maires, "
        f"tandis que **{dep_min['dep']}** affiche le taux le plus bas (**{dep_min['pct_femmes']}%**)."
    )

# ══════════════════════════════════════════════════════
# TAB 3 — Classements
# ══════════════════════════════════════════════════════
with tab3:
    col_g, col_d = st.columns(2)

    dep_stats = (
        maires.groupby("dep")
        .agg(
            total=("sexe", "count"),
            femmes=("sexe", lambda x: (x == "F").sum()),
        )
        .assign(pct_femmes=lambda d: (d["femmes"] / d["total"] * 100).round(1))
        .reset_index()
    )

    with col_g:
        st.subheader("🏆 Top 10 — plus de femmes maires")
        top10 = dep_stats.nlargest(10, "pct_femmes")[["dep", "pct_femmes", "total", "femmes"]]
        top10.columns = ["Département", "% Femmes", "Total maires", "Nb femmes"]
        st.dataframe(top10, use_container_width=True, hide_index=True)

    with col_d:
        st.subheader("⚠️ Flop 10 — moins de femmes maires")
        flop10 = dep_stats.nsmallest(10, "pct_femmes")[["dep", "pct_femmes", "total", "femmes"]]
        flop10.columns = ["Département", "% Femmes", "Total maires", "Nb femmes"]
        st.dataframe(flop10, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Source : RNE — Ministère de l'Intérieur | Licence Ouverte 2.0")