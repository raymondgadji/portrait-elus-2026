"""
pages/1_IRD.py
--------------
Indice de Représentativité Démocratique (IRD) — V4
Deux angles complémentaires :
  - IRD Maires      : score historique (cité dans la presse, V2)
  - IRD Conseillers : score V3 (conseil municipal complet)
Deux référentiels pour l'explorateur commune :
  - IRD local  : vs population de la commune (INSEE 2022)
  - IRD national : vs références nationales françaises
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from utils.loader import charger_maires, charger_conseillers

st.set_page_config(page_title="IRD - Indice de Représentativité", page_icon="🏛️", layout="wide")

LINKEDIN    = "https://www.linkedin.com/in/raymond-gadji/"
INSEE_LIGHT = Path("data/processed/insee_light.csv")

# ── Références nationales (INSEE 2022) ────────────────────────────────────────
REF_PCT_FEMMES = 51.6
REF_AGE_MEDIAN = 42.0
REF_PCT_CADRES = 9.9

# ── Badge & footer ────────────────────────────────────────────────────────────
def afficher_badge_defi():
    st.markdown("""
        <div style="display:flex;justify-content:center;margin:0.5rem 0 1rem 0;">
            <span style="background-color:#003189;color:white;padding:0.4rem 1rem;
                border-radius:20px;font-size:0.8rem;font-weight:600;letter-spacing:0.05em;
                display:flex;align-items:center;gap:0.5rem;">
                <span style="width:8px;height:8px;background:#4CAF50;border-radius:50%;
                    display:inline-block;"></span>
                🏆 LAURÉAT · DÉFI OPEN DATA · DATA.GOUV.FR · ÉLECTIONS MUNICIPALES 2026
            </span>
        </div>""", unsafe_allow_html=True)

def afficher_footer():
    afficher_badge_defi()
    st.markdown("---")
    st.markdown(f"""<div style="text-align:center;padding:0.8rem 0 0.2rem 0;">
        <p style="margin:0;font-size:0.85rem;">© 2026 Créé par
            <a href="{LINKEDIN}" target="_blank"
               style="color:#4A90D9;text-decoration:none;font-weight:600;">Raymond Gadji</a>
            — Data Analyst</p>
        <p style="margin:0.25rem 0 0 0;font-size:0.75rem;color:#888;">
            Sources : RNE (Ministère de l'Intérieur) | Recensement INSEE 2022 | Licence Ouverte 2.0
        </p></div>""", unsafe_allow_html=True)

# ── Chargement INSEE ──────────────────────────────────────────────────────────
def charger_insee_light() -> pd.DataFrame:
    if INSEE_LIGHT.exists():
        return pd.read_csv(INSEE_LIGHT, dtype={"CODGEO": str})
    return pd.DataFrame()

# ── Fonction de calcul IRD générique ─────────────────────────────────────────
def calculer_ird(elus: pd.DataFrame, insee: pd.DataFrame) -> pd.DataFrame:
    elus = elus.copy()
    elus["age"] = pd.to_numeric(elus["age"], errors="coerce")
    elus["code_commune_5"] = elus["code_commune"].astype(str).str.zfill(5)

    profil = elus.groupby(
        ["code_commune_5", "commune", "code_dep", "dep"]
    ).agg(
        nb_elus         = ("sexe", "count"),
        pct_femmes_elus = ("sexe", lambda x: (x == "F").mean() * 100),
        age_moyen_elus  = ("age", "mean"),
    ).reset_index()
    profil["age_moyen_elus"] = profil["age_moyen_elus"].fillna(REF_AGE_MEDIAN)

    def pct_cadres(df_c):
        actifs = df_c[~df_c["csp"].str.lower().str.startswith("ancien", na=False)]
        if len(actifs) == 0:
            return 0
        cadres = actifs["csp"].str.lower().str.contains(
            "cadre|ingénieur|profession libérale|professeur|profession scientifique",
            na=False
        ).sum()
        return cadres / len(actifs) * 100

    csp_par_commune = elus.groupby("code_commune_5").apply(
        pct_cadres, include_groups=False
    ).reset_index()
    csp_par_commune.columns = ["code_commune_5", "pct_cadres_elus"]
    profil = profil.merge(csp_par_commune, on="code_commune_5", how="left")
    profil["pct_cadres_elus"] = profil["pct_cadres_elus"].fillna(0.0)

    # Fusion INSEE
    if not insee.empty:
        insee_copy = insee.copy()
        insee_copy["CODGEO"] = insee_copy["CODGEO"].astype(str).str.zfill(5)
        profil = profil.merge(
            insee_copy.rename(columns={"CODGEO": "code_commune_5"}),
            on="code_commune_5", how="left"
        )

    for col, ref in [("pct_femmes_pop", REF_PCT_FEMMES),
                     ("pct_cadres_pop", REF_PCT_CADRES),
                     ("age_median_pop", REF_AGE_MEDIAN)]:
        if col not in profil.columns:
            profil[col] = ref
        else:
            profil[col] = profil[col].fillna(ref)

    # IRD local
    eg = (profil["pct_femmes_elus"] - profil["pct_femmes_pop"]).abs()
    ea = (profil["age_moyen_elus"]  - profil["age_median_pop"]).abs()
    ec = (profil["pct_cadres_elus"] - profil["pct_cadres_pop"]).abs()

    profil["score_genre"] = (100 - eg.clip(0, 100)).clip(0, 100).round(1)
    profil["score_age"]   = (100 - (ea / 30 * 100)).clip(0, 100).round(1)
    profil["score_csp"]   = (100 - (ec / 25 * 100)).clip(0, 100).round(1)
    profil["ecart_genre"] = eg.round(1)
    profil["ecart_age"]   = ea.round(1)
    profil["ecart_csp"]   = ec.round(1)
    profil["IRD"] = (
        profil["score_genre"] * 0.40 +
        profil["score_age"]   * 0.35 +
        profil["score_csp"]   * 0.25
    ).round(1)

    # IRD national
    eg_n = (profil["pct_femmes_elus"] - REF_PCT_FEMMES).abs()
    ea_n = (profil["age_moyen_elus"]  - REF_AGE_MEDIAN).abs()
    ec_n = (profil["pct_cadres_elus"] - REF_PCT_CADRES).abs()

    profil["score_genre_nat"] = (100 - eg_n.clip(0, 100)).clip(0, 100).round(1)
    profil["score_age_nat"]   = (100 - (ea_n / 30 * 100)).clip(0, 100).round(1)
    profil["score_csp_nat"]   = (100 - (ec_n / 25 * 100)).clip(0, 100).round(1)
    profil["IRD_nat"] = (
        profil["score_genre_nat"] * 0.40 +
        profil["score_age_nat"]   * 0.35 +
        profil["score_csp_nat"]   * 0.25
    ).round(1)

    profil["rang"]     = profil["IRD"].rank(ascending=False, method="min").fillna(0).astype(int)
    profil["rang_nat"] = profil["IRD_nat"].rank(ascending=False, method="min").fillna(0).astype(int)

    return profil.dropna(subset=["IRD"]).sort_values("IRD", ascending=False)


# ── Chargement ───────────────────────────────────────────────────────────────
st.title("🏛️ Indice de Représentativité Démocratique (IRD)")
afficher_badge_defi()

maires      = charger_maires()
conseillers = charger_conseillers()
insee       = charger_insee_light()

st.markdown("""
**Question centrale :** Les élu·es municipaux ressemblent-ils aux habitant·es qu'ils représentent ?

L'IRD mesure l'écart entre le **profil des élus** (genre, âge, CSP) et le **profil de la population**.
Deux angles complémentaires : les **maires** seuls, et le **conseil municipal complet**.
""")

with st.expander("📐 Méthodologie — comment est calculé l'IRD ?"):
    st.markdown(f"""
    ### Formule

    `IRD = (score_genre × 0.40) + (score_âge × 0.35) + (score_CSP × 0.25)`

    | Composante | Mesure | Normalisation | Poids |
    |-----------|--------|--------------|-------|
    | **Genre** | Écart % femmes élues vs % femmes population | Écart / 100 pts | 40% |
    | **Âge** | Écart âge moyen élus vs âge médian population | Écart / 30 ans | 35% |
    | **CSP** | Écart % cadres élus vs % cadres actifs | Écart / 25 pts | 25% |

    **Score 100** = miroir parfait. **Score 0** = aucune ressemblance.

    ### Deux angles de lecture
    - **IRD Maires** : 34 874 maires — score historique, cité dans la presse et par data.gouv.fr
    - **IRD Conseillers** : 485 827 conseillers — image complète du conseil municipal

    ### Références nationales (INSEE 2022)
    **{REF_PCT_FEMMES}%** femmes | **{REF_AGE_MEDIAN} ans** âge médian | **{REF_PCT_CADRES}%** cadres actifs
    """)

# ── Calcul ────────────────────────────────────────────────────────────────────
with st.spinner("Calcul de l'IRD en cours..."):
    ird_maires      = calculer_ird(maires, insee)
    ird_conseillers = calculer_ird(conseillers, insee)

ird_maires      = ird_maires[ird_maires["IRD"] >= 10].copy()
ird_conseillers = ird_conseillers[ird_conseillers["IRD"] >= 10].copy()
nb_communes_m   = len(ird_maires)
nb_communes_c   = len(ird_conseillers)

# ══════════════════════════════════════════════════════════════════════════════
# VUE NATIONALE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 📊 Vue nationale — référentiel national (vs moyennes françaises)")

col_m, col_c = st.columns(2)
ird_m_moy = ird_maires["IRD_nat"].mean()
ird_c_moy = ird_conseillers["IRD_nat"].mean()

with col_m:
    st.markdown("### 👤 IRD Maires")
    st.caption(f"Score historique — {nb_communes_m:,} communes".replace(",", " "))
    st.metric("IRD national moyen", f"{ird_m_moy:.1f}/100")
    k1, k2, k3 = st.columns(3)
    k1.metric("Genre", f"{ird_maires['score_genre_nat'].mean():.1f}")
    k2.metric("Âge",   f"{ird_maires['score_age_nat'].mean():.1f}")
    k3.metric("CSP",   f"{ird_maires['score_csp_nat'].mean():.1f}")
    st.info(f"📰 Score publié et cité dans la presse : **{ird_m_moy:.1f}/100**")
    fig_m = px.histogram(ird_maires, x="IRD_nat", nbins=40,
        color_discrete_sequence=["#457b9d"],
        labels={"IRD_nat": "IRD national", "count": "Communes"},
        title="Distribution IRD national — Maires")
    fig_m.add_vline(x=ird_m_moy, line_dash="dash", line_color="red",
        annotation_text=f"Moy. {ird_m_moy:.1f}", annotation_position="top right")
    st.plotly_chart(fig_m, use_container_width=True)

with col_c:
    st.markdown("### 👥 IRD Conseillers Municipaux")
    st.caption(f"Score V4 — {nb_communes_c:,} communes".replace(",", " "))
    st.metric("IRD national moyen", f"{ird_c_moy:.1f}/100")
    k4, k5, k6 = st.columns(3)
    k4.metric("Genre", f"{ird_conseillers['score_genre_nat'].mean():.1f}")
    k5.metric("Âge",   f"{ird_conseillers['score_age_nat'].mean():.1f}")
    k6.metric("CSP",   f"{ird_conseillers['score_csp_nat'].mean():.1f}")
    st.info(f"📊 Impact loi parité 2025 visible : **{ird_c_moy:.1f}/100**")
    fig_c = px.histogram(ird_conseillers, x="IRD_nat", nbins=40,
        color_discrete_sequence=["#e76f51"],
        labels={"IRD_nat": "IRD national", "count": "Communes"},
        title="Distribution IRD national — Conseillers")
    fig_c.add_vline(x=ird_c_moy, line_dash="dash", line_color="red",
        annotation_text=f"Moy. {ird_c_moy:.1f}", annotation_position="top right")
    st.plotly_chart(fig_c, use_container_width=True)

# Explication de l'écart
pct_f_maires = (maires["sexe"] == "F").mean() * 100
pct_f_cons   = (conseillers["sexe"] == "F").mean() * 100
st.markdown("---")
st.info(
    f"**Pourquoi cet écart de {abs(ird_c_moy - ird_m_moy):.1f} points entre maires et conseillers ?**  \n"
    f"Les **maires** sont à **{pct_f_maires:.1f}%** de femmes vs **{pct_f_cons:.1f}%** "
    f"pour les **conseillers**. La loi du 21 mai 2025 impose la parité dans les listes municipales "
    f"(y compris communes < 1 000 hab.), ce qui améliore fortement le score genre des conseils "
    f"sans impacter l'élection des maires qui reste libre."
)

# ══════════════════════════════════════════════════════════════════════════════
# ONGLETS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 🔍 Analyse détaillée")
tab1, tab2, tab3 = st.tabs(["Classements", "Par département", "Ma commune"])

with tab1:
    angle = st.radio("Calculé sur :",
        ["👤 Maires", "👥 Conseillers municipaux"], horizontal=True)
    df_t  = ird_maires if "Maires" in angle else ird_conseillers
    nb_t  = nb_communes_m if "Maires" in angle else nb_communes_c

    cg, cd = st.columns(2)
    with cg:
        st.subheader("🏆 Top 20")
        t = df_t.head(20)[["commune","dep","IRD_nat","score_genre_nat","score_age_nat","score_csp_nat","nb_elus"]].copy()
        t.columns = ["Commune","Dép.","IRD","Genre","Âge","CSP","Nb élus"]
        st.dataframe(t, use_container_width=True, hide_index=True)
    with cd:
        st.subheader("⚠️ Flop 20")
        f = df_t.nsmallest(20,"IRD_nat")[["commune","dep","IRD_nat","score_genre_nat","score_age_nat","score_csp_nat","nb_elus"]].copy()
        f.columns = ["Commune","Dép.","IRD","Genre","Âge","CSP","Nb élus"]
        st.dataframe(f, use_container_width=True, hide_index=True)

with tab2:
    angle2 = st.radio("Calculé sur :",
        ["👤 Maires", "👥 Conseillers municipaux"], horizontal=True, key="r2")
    df_d = ird_maires if "Maires" in angle2 else ird_conseillers
    ird_dep = df_d.groupby("dep")["IRD_nat"].mean().round(1).reset_index().sort_values("IRD_nat")
    fig_dep = px.bar(ird_dep, x="IRD_nat", y="dep", orientation="h",
        color="IRD_nat", color_continuous_scale=["#e76f51","#e9c46a","#2a9d8f"],
        range_color=[30,100],
        labels={"IRD_nat":"IRD moyen","dep":"Département"},
        title=f"IRD national moyen par département — {'Maires' if 'Maires' in angle2 else 'Conseillers'}",
        height=1600, text="IRD_nat")
    fig_dep.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig_dep.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_dep, use_container_width=True)

with tab3:
    angle3 = st.radio("Calculé sur :",
        ["👤 Maires", "👥 Conseillers municipaux"], horizontal=True, key="r3")
    df_s  = ird_maires if "Maires" in angle3 else ird_conseillers
    nb_s  = nb_communes_m if "Maires" in angle3 else nb_communes_c

    commune_input = st.text_input("Tapez le nom d'une commune :",
        placeholder="Ex : Paris, Lyon, Bordeaux...")

    if commune_input and len(commune_input) >= 2:
        resultats = df_s[df_s["commune"].str.contains(commune_input, case=False, na=False)].head(20)

        if resultats.empty:
            st.warning(f"Aucune commune trouvée pour « {commune_input} ».")
        else:
            for _, row in resultats.iterrows():
                ird_loc = row["IRD"]
                ird_nat = row["IRD_nat"]
                couleur = "#2a9d8f" if ird_nat >= 70 else "#e9c46a" if ird_nat >= 50 else "#e76f51"
                emoji   = "🟢" if ird_nat >= 70 else "🟡" if ird_nat >= 50 else "🔴"

                with st.expander(
                    f"{emoji} **{row['commune']}** ({row['dep']}) — "
                    f"IRD local : {ird_loc}/100 | IRD national : {ird_nat}/100"
                ):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("#### 📍 IRD local")
                        st.caption("vs population de cette commune")
                        st.markdown(f"**{ird_loc}/100**")
                        st.progress(int(ird_loc)/100)
                        st.markdown(f"Rang : **{row['rang']:,}/{nb_s:,}**".replace(",", " "))
                        st.markdown(f"Nb élus : {row['nb_elus']}")
                        st.markdown("---")
                        for nom, score, detail in [
                            ("Genre", row["score_genre"], f"{row['ecart_genre']:.1f} pts d'écart"),
                            ("Âge",   row["score_age"],   f"{row['ecart_age']:.1f} ans d'écart"),
                            ("CSP",   row["score_csp"],   f"{row['ecart_csp']:.1f} pts d'écart"),
                        ]:
                            e = "🟢" if score>=70 else "🟡" if score>=50 else "🔴"
                            st.markdown(f"{e} **{nom}** — {score:.0f}/100  \n"
                                f"<small style='color:#888'>{detail}</small>", unsafe_allow_html=True)
                            st.progress(int(score)/100)

                    with c2:
                        st.markdown("#### 🇫🇷 IRD national")
                        st.caption("vs références françaises")
                        st.markdown(f"**{ird_nat}/100**")
                        st.progress(int(ird_nat)/100)
                        st.markdown(f"Rang : **{row['rang_nat']:,}/{nb_s:,}**".replace(",", " "))
                        st.markdown(f"Réf. : {REF_PCT_FEMMES}% | {REF_AGE_MEDIAN} ans | {REF_PCT_CADRES}%")
                        st.markdown("---")
                        for nom, score, detail in [
                            ("Genre", row["score_genre_nat"], f"vs {REF_PCT_FEMMES}% femmes"),
                            ("Âge",   row["score_age_nat"],   f"vs {REF_AGE_MEDIAN} ans"),
                            ("CSP",   row["score_csp_nat"],   f"vs {REF_PCT_CADRES}% cadres"),
                        ]:
                            e = "🟢" if score>=70 else "🟡" if score>=50 else "🔴"
                            st.markdown(f"{e} **{nom}** — {score:.0f}/100  \n"
                                f"<small style='color:#888'>{detail}</small>", unsafe_allow_html=True)
                            st.progress(int(score)/100)

                        categories = ["Genre", "Âge", "CSP"]
                        values = [row["score_genre_nat"], row["score_age_nat"], row["score_csp_nat"]]
                        fig_r = go.Figure(data=go.Scatterpolar(
                            r=values+[values[0]], theta=categories+[categories[0]],
                            fill="toself", fillcolor=couleur, opacity=0.3,
                            line=dict(color=couleur, width=2)))
                        fig_r.add_trace(go.Scatterpolar(
                            r=[100,100,100,100], theta=categories+[categories[0]],
                            fill="toself", fillcolor="rgba(200,200,200,0.1)",
                            line=dict(color="gray", dash="dot", width=1), showlegend=False))
                        fig_r.update_layout(
                            polar=dict(radialaxis=dict(visible=True, range=[0,100])),
                            showlegend=False, height=260,
                            margin=dict(l=20,r=20,t=30,b=20))
                        st.plotly_chart(fig_r, use_container_width=True)
    else:
        st.info("Entrez au moins 2 caractères pour rechercher une commune.")

afficher_footer()