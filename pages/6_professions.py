"""
pages/3_Professions.py  —  CSP des élu·es
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

st.set_page_config(page_title="Professions", page_icon="💼", layout="wide")
st.title("💼 Professions des élu·es")
st.markdown(
    "Les élu·es municipaux représentent-ils toutes les catégories socio-professionnelles "
    "de la société française ? Quels métiers sont sur- ou sous-représentés ?"
)

maires      = charger_maires()
conseillers = charger_conseillers()

def regrouper_csp(csp_libelle: str) -> str:
    if pd.isna(csp_libelle):
        return "Non renseigné"
    c = str(csp_libelle).lower()
    if "agricult" in c:
        return "Agriculteurs"
    if "artisan" in c or "commerc" in c or "chef d'entr" in c or "patron" in c:
        return "Artisans / Commerçants"
    if ("cadre" in c or "ingénieur" in c or "chef d'établ" in c
            or "profession libérale" in c or "médecin" in c
            or "pharmacien" in c or "architecte" in c or "avocat" in c):
        return "Cadres & Prof. intellectuelles"
    if ("intermédiai" in c or "technicien" in c or "instituteur" in c
            or "infirmier" in c or "assistant" in c):
        return "Professions intermédiaires"
    if "employé" in c or "secrétaire" in c or "agent de service" in c:
        return "Employés"
    if "ouvrier" in c:
        return "Ouvriers"
    if "ancien" in c or "retraité" in c:
        return "Retraités / Anciens"
    if "sans activité" in c or "chômeur" in c or "élève" in c or "étudiant" in c:
        return "Sans activité / Étudiants"
    return "Autres"

maires["csp_groupe"]      = maires["csp"].apply(regrouper_csp)
conseillers["csp_groupe"] = conseillers["csp"].apply(regrouper_csp)

tab1, tab2, tab3 = st.tabs(["Vue globale", "Détail par CSP", "Comparaison INSEE"])

# ══════════════════════════════════════════════════════
# TAB 1 — Vue globale avec phrases
# ══════════════════════════════════════════════════════
with tab1:
    col_g, col_d = st.columns(2)

    with col_g:
        st.subheader("Maires — grandes catégories")
        csp_m = maires["csp_groupe"].value_counts().reset_index()
        csp_m.columns = ["CSP", "Nombre"]
        csp_m["Pct"] = (csp_m["Nombre"] / csp_m["Nombre"].sum() * 100).round(1)
        fig = px.pie(csp_m, names="CSP", values="Nombre", hole=0.4,
                     title="Répartition CSP — maires",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    with col_d:
        st.subheader("Conseillers — grandes catégories")
        csp_c = conseillers["csp_groupe"].value_counts().reset_index()
        csp_c.columns = ["CSP", "Nombre"]
        csp_c["Pct"] = (csp_c["Nombre"] / csp_c["Nombre"].sum() * 100).round(1)
        fig2 = px.pie(csp_c, names="CSP", values="Nombre", hole=0.4,
                      title="Répartition CSP — conseillers",
                      color_discrete_sequence=px.colors.qualitative.Set2)
        fig2.update_traces(textinfo="percent+label")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Phrases pour chaque catégorie ─────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📝 Ce que révèlent les données — maires")

    # Calcul dynamique des pourcentages
    total_m = len(maires)
    pct = {row["CSP"]: row["Pct"] for _, row in csp_m.iterrows()}

    def p(cat): return pct.get(cat, 0.0)

    st.markdown(f"""
    - **Cadres & professions intellectuelles supérieures ({p('Cadres & Prof. intellectuelles'):.1f}%) :**
      Ce groupe — qui inclut les ingénieurs, médecins, avocats, architectes et dirigeants d'entreprise —
      est très largement sur-représenté parmi les maires. Il ne représente qu'environ 18% de la
      population active en France, mais constitue près d'**un maire sur cinq**.

    - **Agriculteurs ({p('Agriculteurs'):.1f}%) :**
      Les agriculteurs sont très présents dans les mairies, bien au-delà de leur poids dans la
      population active nationale (environ 1,5%). Cela s'explique par la forte proportion de
      petites communes rurales en France où les agriculteurs jouent un rôle central.

    - **Artisans / Commerçants ({p('Artisans / Commerçants'):.1f}%) :**
      Cette catégorie est représentée de façon légèrement supérieure à son poids dans la
      population active (environ 6,5%), reflétant l'ancrage local des chefs de petites entreprises.

    - **Professions intermédiaires ({p('Professions intermédiaires'):.1f}%) :**
      Techniciens, infirmiers, instituteurs — ces métiers du quotidien restent peu représentés
      malgré leur importance numérique dans la société (environ 25% de la population active).

    - **Employés ({p('Employés'):.1f}%) :**
      Avec environ 27% de la population active, les employés sont pourtant parmi les plus
      sous-représentés dans les mairies. Moins de disponibilité, ressources et réseaux
      expliquent en partie cette absence.

    - **Ouvriers ({p('Ouvriers'):.1f}%) :**
      Les ouvriers représentent environ 20% de la population active mais sont quasi absents
      des mairies. Ce fossé illustre les inégalités persistantes d'accès aux mandats électifs.

    - **Retraités / Anciens ({p('Retraités / Anciens'):.1f}%) :**
      Une part notable des maires sont d'anciens actifs (souvent d'anciens cadres ou
      fonctionnaires). La disponibilité liée à la retraite facilite l'engagement municipal.
    """)

    st.info(
        "**En résumé :** Les mairies françaises sont dominées par des profils diplômés, "
        "indépendants ou retraités. Les catégories populaires — ouvriers, employés — y sont "
        "quasi absentes, révélant un déficit de représentativité sociale."
    )

# ══════════════════════════════════════════════════════
# TAB 2 — Détail complet
# ══════════════════════════════════════════════════════
with tab2:
    choix = st.radio("Afficher pour :", ["Maires", "Conseillers"], horizontal=True)
    df_choix = maires if choix == "Maires" else conseillers

    csp_detail = df_choix["csp"].value_counts().reset_index()
    csp_detail.columns = ["CSP", "Nombre"]
    csp_detail["Pct"] = (csp_detail["Nombre"] / csp_detail["Nombre"].sum() * 100).round(2)
    csp_detail = csp_detail.head(30)

    fig_bar = px.bar(
        csp_detail,
        x="Pct", y="CSP", orientation="h",
        color="Pct",
        color_continuous_scale="Blues",
        labels={"Pct": "% des élus", "CSP": ""},
        title=f"Top 30 des professions — {choix}",
        height=900,
        text="Pct",
    )
    fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_bar.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# ══════════════════════════════════════════════════════
# TAB 3 — Comparaison vs INSEE
# ══════════════════════════════════════════════════════
with tab3:
    st.subheader("Représentativité vs population active (INSEE 2023)")
    st.caption(
        "⚠️ Comparaison approximative — les catégories RNE et INSEE ne sont pas strictement équivalentes."
    )

    csp_m_pct = (
        maires["csp_groupe"]
        .value_counts(normalize=True)
        .mul(100).round(1)
        .reset_index()
    )
    csp_m_pct.columns = ["CSP", "Pct_elus"]

    fig_comp = px.bar(
        csp_m_pct.sort_values("Pct_elus", ascending=True),
        x="Pct_elus", y="CSP", orientation="h",
        color="Pct_elus",
        color_continuous_scale="Oranges",
        labels={"Pct_elus": "% parmi les maires", "CSP": ""},
        title="Part de chaque CSP parmi les maires",
        text="Pct_elus",
        height=500,
    )
    fig_comp.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_comp.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown(
        "**Observation clé :** Les **retraités et anciens cadres** représentent une part "
        "disproportionnée des maires. À l'inverse, les **ouvriers**, **employés** et "
        "**jeunes actifs** sont nettement sous-représentés. "
        "Cette distorsion traduit des **inégalités d'accès aux mandats électifs** liées "
        "au niveau d'études, au temps disponible et aux réseaux sociaux."
    )

afficher_footer()