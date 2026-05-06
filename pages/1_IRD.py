"""
pages/1_IRD.py
--------------
Indice de Représentativité Démocratique (IRD) — V3
Score synthétique mesurant à quel point les élus ressemblent à leurs administrés.
Données : RNE (Ministère de l'Intérieur) x INSEE par commune (insee_light.csv)

V3 : IRD calculé sur les CONSEILLERS MUNICIPAUX (pas seulement le maire)
     Deux scores présentés pour une approche scientifique complète :
     - IRD local  : comparaison à la population de chaque commune (INSEE 2022)
     - IRD national : comparaison aux moyennes nationales françaises

Formule IRD (0 = très peu représentatif, 100 = parfaitement représentatif) :
  IRD = score_genre×40% + score_âge×35% + score_CSP×25%
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from utils.loader import charger_maires, charger_conseillers

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="IRD - Indice de Représentativité", page_icon="🏛️", layout="wide")

LINKEDIN = "https://www.linkedin.com/in/raymond-gadji/"
INSEE_LIGHT = Path("data/processed/insee_light.csv")

# Références nationales françaises (sources INSEE 2022)
REF_PCT_FEMMES = 51.6   # % femmes dans la population française
REF_AGE_MEDIAN = 42.0   # âge médian France métropolitaine
REF_PCT_CADRES = 9.9    # % cadres actifs — médiane nationale INSEE 2022

def afficher_badge_defi():
    st.markdown(
        """
        <div style="display:flex;justify-content:center;margin:0.5rem 0 1rem 0;">
            <span style="
                background-color:#003189;
                color:white;
                padding:0.4rem 1rem;
                border-radius:20px;
                font-size:0.8rem;
                font-weight:600;
                letter-spacing:0.05em;
                display:flex;
                align-items:center;
                gap:0.5rem;
            ">
                <span style="
                    width:8px;height:8px;
                    background:#4CAF50;
                    border-radius:50%;
                    display:inline-block;
                "></span>
                🏆 LAURÉAT · DÉFI OPEN DATA · DATA.GOUV.FR · ÉLECTIONS MUNICIPALES 2026
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def afficher_footer():
    afficher_badge_defi()
    st.markdown("---")
    st.markdown(
        f"""<div style="text-align:center;padding:0.8rem 0 0.2rem 0;">
            <p style="margin:0;font-size:0.85rem;">
                © 2026 Créé par <a href="{LINKEDIN}" target="_blank"
                style="color:#4A90D9;text-decoration:none;font-weight:600;">Raymond Gadji</a>
                — Data Analyst</p>
            <p style="margin:0.25rem 0 0 0;font-size:0.75rem;color:#888;">
                Sources : RNE (Ministère de l'Intérieur) | Recensement INSEE 2022
                | Licence Ouverte 2.0</p>
        </div>""",
        unsafe_allow_html=True,
    )

# ── Titre & explication ───────────────────────────────────────────────────────
st.title("🏛️ Indice de Représentativité Démocratique (IRD)")
afficher_badge_defi()
st.markdown("""
**Question centrale :** Les élu·es municipaux ressemblent-ils aux habitant·es qu'ils représentent ?

L'IRD mesure l'écart entre le **profil des conseillers municipaux** (genre, âge, CSP)
et le **profil de la population**. Deux référentiels sont présentés pour une lecture complète.
""")

with st.expander("📐 Méthodologie — comment est calculé l'IRD ?"):
    st.markdown("""
    ### Formule générale

    L'IRD combine **3 composantes** normalisées de 0 à 100, pondérées selon leur importance démocratique :

    | Composante | Mesure | Normalisation | Poids |
    |-----------|--------|--------------|-------|
    | **Genre** | Écart % femmes élues vs % femmes population | Écart / 100 pts | 40% |
    | **Âge** | Écart âge moyen élus vs âge médian population | Écart / 30 ans | 35% |
    | **CSP** | Écart % cadres élus vs % cadres actifs population | Écart / 50 pts | 25% |

    `IRD = (score_genre × 0.40) + (score_âge × 0.35) + (score_CSP × 0.25)`

    ---

    ### Deux référentiels scientifiques

    **IRD local** — *"Les élus ressemblent-ils à leur propre commune ?"*
    Chaque commune est comparée à **sa propre population locale** (INSEE 2022 par commune).
    Ce score mesure la représentativité interne : est-ce que le conseil municipal reflète
    la réalité démographique locale ?

    **IRD national** — *"Les élus ressemblent-ils à la France ?"*
    Toutes les communes sont comparées aux **moyennes nationales françaises** :
    - % femmes : 51.6% (population française)
    - Âge médian : 42 ans (France métropolitaine)
    - % cadres actifs : 9.9% (médiane nationale INSEE 2022)

    Ce score mesure la représentativité par rapport à un étalon national commun.

    ---

    ### Données sources
    - Profil des élus : **Répertoire National des Élus** (RNE), Ministère de l'Intérieur — V3 basée sur les conseillers municipaux (pas uniquement le maire)
    - Profil population locale : **Recensement INSEE 2022** par commune
    - Références nationales : **INSEE 2022** (moyennes et médianes françaises)
    """)

# ── Chargement INSEE ──────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Chargement des données INSEE par commune...")
def charger_insee_light() -> pd.DataFrame:
    if INSEE_LIGHT.exists():
        return pd.read_csv(INSEE_LIGHT, dtype={"CODGEO": str})
    return pd.DataFrame()

# ── Calcul IRD ────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Calcul de l'IRD par commune...")
def calculer_ird(conseillers: pd.DataFrame, insee: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule deux scores IRD pour chaque commune :
    - IRD     : comparaison à la population locale (INSEE par commune)
    - IRD_nat : comparaison aux références nationales françaises
    """
    conseillers = conseillers.copy()
    conseillers["age"] = pd.to_numeric(conseillers["age"], errors="coerce")
    conseillers["code_commune_5"] = (
        conseillers["code_dep"].astype(str).str.zfill(2) +
        conseillers["code_commune"].astype(str).str.zfill(3)
    )

    # ── Profil des conseillers par commune ───────────────────────────────
    profil_elus = conseillers.groupby(
        ["code_commune_5", "commune", "code_dep", "dep"]
    ).agg(
        nb_elus         = ("sexe", "count"),
        pct_femmes_elus = ("sexe", lambda x: (x == "F").mean() * 100),
        age_moyen_elus  = ("age",  "mean"),
    ).reset_index()

    profil_elus["age_moyen_elus"] = profil_elus["age_moyen_elus"].fillna(REF_AGE_MEDIAN)

    def pct_cadres(df_commune):
        total = len(df_commune)
        if total == 0:
            return 0
        actifs = df_commune[~df_commune["csp"].str.lower().str.startswith("ancien", na=False)]
        if len(actifs) == 0:
            return 0
        cadres = actifs["csp"].str.lower().str.contains(
            "cadre|ingénieur|profession libérale|professeur|profession scientifique",
            na=False
        ).sum()
        return cadres / len(actifs) * 100

    csp_elus = conseillers.groupby("code_commune_5").apply(pct_cadres).reset_index()
    csp_elus.columns = ["code_commune_5", "pct_cadres_elus"]
    profil_elus = profil_elus.merge(csp_elus, on="code_commune_5", how="left")
    profil_elus["pct_cadres_elus"] = profil_elus["pct_cadres_elus"].fillna(0.0)

    # ── Fusion avec INSEE par commune ─────────────────────────────────────
    if not insee.empty:
        insee = insee.copy()
        insee["CODGEO"] = insee["CODGEO"].astype(str).str.zfill(5)
        profil_elus = profil_elus.merge(
            insee.rename(columns={"CODGEO": "code_commune_5"}),
            on="code_commune_5",
            how="left"
        )
        profil_elus["pct_femmes_pop"] = profil_elus["pct_femmes_pop"].fillna(REF_PCT_FEMMES)
        profil_elus["pct_cadres_pop"] = profil_elus["pct_cadres_pop"].fillna(REF_PCT_CADRES)
        profil_elus["age_median_pop"] = profil_elus["age_median_pop"].fillna(REF_AGE_MEDIAN)
    else:
        profil_elus["pct_femmes_pop"] = REF_PCT_FEMMES
        profil_elus["pct_cadres_pop"] = REF_PCT_CADRES
        profil_elus["age_median_pop"] = REF_AGE_MEDIAN

    # ── Score IRD local (comparaison à la population locale) ──────────────
    ecart_genre = (profil_elus["pct_femmes_elus"] - profil_elus["pct_femmes_pop"]).abs()
    score_genre = (100 - ecart_genre.clip(0, 100)).clip(0, 100)

    ecart_age = (profil_elus["age_moyen_elus"] - profil_elus["age_median_pop"]).abs()
    score_age = (100 - (ecart_age / 30 * 100)).clip(0, 100)

    ecart_csp = (profil_elus["pct_cadres_elus"] - profil_elus["pct_cadres_pop"]).abs()
    score_csp = (100 - (ecart_csp / 50 * 100)).clip(0, 100)

    profil_elus["IRD"] = (
        score_genre * 0.40 + score_age * 0.35 + score_csp * 0.25
    ).round(1)

    profil_elus["score_genre"] = score_genre.round(1)
    profil_elus["score_age"]   = score_age.round(1)
    profil_elus["score_csp"]   = score_csp.round(1)
    profil_elus["ecart_genre"] = ecart_genre.round(1)
    profil_elus["ecart_age"]   = ecart_age.round(1)
    profil_elus["ecart_csp"]   = ecart_csp.round(1)

    # ── Score IRD national (comparaison aux références nationales) ────────
    ecart_genre_nat = (profil_elus["pct_femmes_elus"] - REF_PCT_FEMMES).abs()
    score_genre_nat = (100 - ecart_genre_nat.clip(0, 100)).clip(0, 100)

    ecart_age_nat = (profil_elus["age_moyen_elus"] - REF_AGE_MEDIAN).abs()
    score_age_nat = (100 - (ecart_age_nat / 30 * 100)).clip(0, 100)

    ecart_csp_nat = (profil_elus["pct_cadres_elus"] - REF_PCT_CADRES).abs()
    score_csp_nat = (100 - (ecart_csp_nat / 50 * 100)).clip(0, 100)

    profil_elus["IRD_nat"] = (
        score_genre_nat * 0.40 + score_age_nat * 0.35 + score_csp_nat * 0.25
    ).round(1)

    profil_elus["score_genre_nat"] = score_genre_nat.round(1)
    profil_elus["score_age_nat"]   = score_age_nat.round(1)
    profil_elus["score_csp_nat"]   = score_csp_nat.round(1)

    profil_elus["rang"] = profil_elus["IRD"].rank(
        ascending=False, method="min"
    ).fillna(0).astype(int)

    profil_elus["rang_nat"] = profil_elus["IRD_nat"].rank(
        ascending=False, method="min"
    ).fillna(0).astype(int)

    return profil_elus.sort_values("IRD", ascending=False)


# ── Chargement ────────────────────────────────────────────────────────────────
maires      = charger_maires()
conseillers = charger_conseillers()
insee       = charger_insee_light()

if insee.empty:
    st.warning("Données INSEE par commune non trouvées — utilisation des moyennes nationales.")

ird_df = calculer_ird(conseillers, insee)
ird_df = ird_df.dropna(subset=["IRD"])
ird_df = ird_df[ird_df["IRD"] >= 10].copy()
nb_communes = len(ird_df)

if ird_df.empty:
    st.error("Impossible de calculer l'IRD. Vérifiez les données.")
    st.stop()

# ── KPIs globaux ──────────────────────────────────────────────────────────────
st.markdown("## 📊 Vue nationale")

ird_moy     = ird_df["IRD"].mean()
ird_nat_moy = ird_df["IRD_nat"].mean()
ird_med     = ird_df["IRD"].median()
pct_faible  = (ird_df["IRD_nat"] < 40).mean() * 100
pct_bon     = (ird_df["IRD_nat"] >= 70).mean() * 100

# Deux scores mis en avant
col_loc, col_nat = st.columns(2)
with col_loc:
    st.metric(
        "IRD local moyen",
        f"{ird_moy:.1f}/100",
        help="Comparaison à la population de chaque commune (INSEE 2022)"
    )
    st.caption("Les élus ressemblent-ils à leurs propres administrés ?")

with col_nat:
    st.metric(
        "IRD national moyen",
        f"{ird_nat_moy:.1f}/100",
        help="Comparaison aux références nationales françaises (INSEE 2022)"
    )
    st.caption("Les élus ressemblent-ils à la France ?")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Communes analysées", f"{nb_communes:,}".replace(",", " "))
col2.metric("IRD national médian", f"{ird_df['IRD_nat'].median():.1f}/100")
col3.metric("Communes IRD nat. < 40", f"{pct_faible:.1f}%", help="Représentativité faible vs France")
col4.metric("Communes IRD nat. ≥ 70", f"{pct_bon:.1f}%", help="Bonne représentativité vs France")

# ── Onglets ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["Distribution", "Classements", "Analyse", "Ma commune"])

# ══════════════════════════════════════════════════════
# TAB 1 — Distribution des IRD
# ══════════════════════════════════════════════════════
with tab1:

    st.markdown("### Distribution des deux scores IRD")
    col_g, col_d = st.columns(2)

    with col_g:
        fig_hist_loc = px.histogram(
            ird_df, x="IRD", nbins=50,
            color_discrete_sequence=["#457b9d"],
            labels={"IRD": "Score IRD local", "count": "Nb communes"},
            title=f"IRD local — comparaison à la population locale",
        )
        fig_hist_loc.add_vline(x=ird_moy, line_dash="dash", line_color="red",
                               annotation_text=f"Moyenne : {ird_moy:.1f}",
                               annotation_position="top right")
        st.plotly_chart(fig_hist_loc, use_container_width=True)

    with col_d:
        fig_hist_nat = px.histogram(
            ird_df, x="IRD_nat", nbins=50,
            color_discrete_sequence=["#e76f51"],
            labels={"IRD_nat": "Score IRD national", "count": "Nb communes"},
            title=f"IRD national — comparaison aux références françaises",
        )
        fig_hist_nat.add_vline(x=ird_nat_moy, line_dash="dash", line_color="red",
                               annotation_text=f"Moyenne : {ird_nat_moy:.1f}",
                               annotation_position="top right")
        st.plotly_chart(fig_hist_nat, use_container_width=True)

    st.markdown("### Contribution de chaque composante à l'IRD national")
    composantes = pd.DataFrame({
        "Composante"          : ["Genre (40%)", "Âge (35%)", "CSP (25%)"],
        "Score moyen national": [
            ird_df["score_genre_nat"].mean().round(1),
            ird_df["score_age_nat"].mean().round(1),
            ird_df["score_csp_nat"].mean().round(1),
        ]
    })
    fig_comp = px.bar(
        composantes, x="Composante", y="Score moyen national",
        color="Score moyen national",
        color_continuous_scale=["#e76f51", "#e9c46a", "#2a9d8f"],
        range_y=[0, 100],
        text="Score moyen national",
        title="Score moyen par composante — référentiel national (100 = parfaitement représentatif)",
    )
    fig_comp.update_traces(textposition="outside")
    fig_comp.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_comp, use_container_width=True)

    score_g = ird_df["score_genre_nat"].mean()
    score_a = ird_df["score_age_nat"].mean()
    score_c = ird_df["score_csp_nat"].mean()
    plus_faible = min(
        [("le genre", score_g), ("l'âge", score_a), ("la CSP", score_c)],
        key=lambda x: x[1]
    )
    st.info(
        f"**Lecture (référentiel national) :** Avec un IRD national moyen de **{ird_nat_moy:.1f}/100**, "
        f"les conseils municipaux français présentent une représentativité "
        f"**{'faible' if ird_nat_moy < 45 else 'moyenne' if ird_nat_moy < 65 else 'correcte'}** "
        f"par rapport aux moyennes nationales. "
        f"La composante la plus déficitaire est **{plus_faible[0]}** "
        f"(score moyen : {plus_faible[1]:.1f}/100)."
    )


# ══════════════════════════════════════════════════════
# TAB 2 — Classements
# ══════════════════════════════════════════════════════
with tab2:

    referentiel = st.radio(
        "Référentiel de classement :",
        ["IRD local (vs population locale)", "IRD national (vs moyennes françaises)"],
        horizontal=True
    )

    col_score = "IRD" if "local" in referentiel else "IRD_nat"
    col_rang  = "rang" if "local" in referentiel else "rang_nat"

    ird_sorted = ird_df.sort_values(col_score, ascending=False)

    col_g, col_d = st.columns(2)
    with col_g:
        st.subheader("🏆 Top 20 — communes les plus représentatives")
        top20 = ird_sorted.head(20)[
            ["commune", "dep", col_score, "score_genre", "score_age", "score_csp", "nb_elus"]
        ].copy()
        top20.columns = ["Commune", "Département", "IRD", "Genre", "Âge", "CSP", "Nb élus"]
        st.dataframe(top20, use_container_width=True, hide_index=True)

    with col_d:
        st.subheader("Flop 20 — communes les moins représentatives")
        flop20 = ird_sorted.tail(20).sort_values(col_score)[
            ["commune", "dep", col_score, "score_genre", "score_age", "score_csp", "nb_elus"]
        ].copy()
        flop20.columns = ["Commune", "Département", "IRD", "Genre", "Âge", "CSP", "Nb élus"]
        st.dataframe(flop20, use_container_width=True, hide_index=True)

    st.markdown("### IRD moyen par département")
    ird_dep = (
        ird_df.groupby("dep")[col_score]
        .mean().round(1).reset_index()
        .sort_values(col_score, ascending=True)
    )
    fig_dep = px.bar(
        ird_dep, x=col_score, y="dep", orientation="h",
        color=col_score,
        color_continuous_scale=["#e76f51", "#e9c46a", "#2a9d8f"],
        range_color=[30, 80],
        labels={col_score: "Score IRD moyen", "dep": "Département"},
        title=f"IRD moyen par département — {referentiel}",
        height=1600,
        text=col_score,
    )
    fig_dep.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig_dep.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_dep, use_container_width=True)


# ══════════════════════════════════════════════════════
# TAB 3 — Analyse approfondie
# ══════════════════════════════════════════════════════
with tab3:
    st.markdown("### IRD selon la taille des communes")

    ird_df_box = ird_df.copy()
    ird_df_box["nb_conseillers"] = ird_df_box["nb_elus"]

    def taille_commune(nb):
        if nb <= 7:  return "Très petites (<=7)"
        if nb <= 15: return "Petites (8-15)"
        if nb <= 23: return "Moyennes (16-23)"
        if nb <= 33: return "Grandes (24-33)"
        return "Très grandes (>33)"

    ird_df_box["taille"] = ird_df_box["nb_conseillers"].apply(taille_commune)
    ordre_tailles = ["Très petites (<=7)", "Petites (8-15)", "Moyennes (16-23)",
                     "Grandes (24-33)", "Très grandes (>33)"]

    col_g, col_d = st.columns(2)
    with col_g:
        fig_box_loc = px.box(
            ird_df_box, x="taille", y="IRD", color="taille",
            color_discrete_sequence=px.colors.qualitative.Set2,
            title="IRD local selon la taille de commune",
            labels={"taille": "Taille", "IRD": "IRD local"},
            category_orders={"taille": ordre_tailles},
        )
        fig_box_loc.update_layout(showlegend=False)
        st.plotly_chart(fig_box_loc, use_container_width=True)

    with col_d:
        fig_box_nat = px.box(
            ird_df_box, x="taille", y="IRD_nat", color="taille",
            color_discrete_sequence=px.colors.qualitative.Set2,
            title="IRD national selon la taille de commune",
            labels={"taille": "Taille", "IRD_nat": "IRD national"},
            category_orders={"taille": ordre_tailles},
        )
        fig_box_nat.update_layout(showlegend=False)
        st.plotly_chart(fig_box_nat, use_container_width=True)

    st.markdown("### Relation IRD — parité femmes/hommes")
    fig_scatter = px.scatter(
        ird_df.sample(min(3000, len(ird_df)), random_state=42),
        x="pct_femmes_elus", y="IRD_nat",
        color="score_genre_nat",
        color_continuous_scale=["#e76f51", "#2a9d8f"],
        hover_data=["commune", "dep"],
        labels={
            "pct_femmes_elus": "% femmes parmi les conseillers",
            "IRD_nat": "IRD national",
            "score_genre_nat": "Score genre (nat.)",
        },
        title="IRD national en fonction du % de femmes conseillères",
        opacity=0.6,
    )
    fig_scatter.add_vline(x=REF_PCT_FEMMES, line_dash="dash", line_color="blue",
                          annotation_text=f"{REF_PCT_FEMMES}% (référence nationale)",
                          annotation_position="top right")
    st.plotly_chart(fig_scatter, use_container_width=True)


# ══════════════════════════════════════════════════════
# TAB 4 — Recherche par commune
# ══════════════════════════════════════════════════════
with tab4:
    st.markdown("### Rechercher une commune")
    commune_input = st.text_input(
        "Tapez le nom d'une commune :",
        placeholder="Ex : Paris, Lyon, Bordeaux, Rouen...",
    )

    if commune_input and len(commune_input) >= 2:
        resultats = ird_df[
            ird_df["commune"].str.contains(commune_input, case=False, na=False)
        ].head(20)

        if resultats.empty:
            st.warning(f"Aucune commune trouvée pour « {commune_input} ».")
        else:
            for _, row in resultats.iterrows():
                ird_val     = row["IRD"]
                ird_nat_val = row["IRD_nat"]
                couleur = "#2a9d8f" if ird_nat_val >= 70 else "#e9c46a" if ird_nat_val >= 50 else "#e76f51"
                emoji   = "🟢" if ird_nat_val >= 70 else "🟡" if ird_nat_val >= 50 else "🔴"

                with st.expander(
                    f"{emoji} **{row['commune']}** ({row['dep']}) — "
                    f"IRD local : {ird_val}/100 | IRD national : {ird_nat_val}/100"
                ):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("#### 📍 IRD local")
                        st.caption("Comparaison à la population de cette commune")
                        st.markdown(f"**Score : {ird_val}/100**")
                        st.progress(int(ird_val) / 100)
                        st.markdown(f"Rang local : **{row['rang']:,}/{nb_communes:,}**".replace(",", " "))
                        st.markdown(f"Nombre de conseillers : {row['nb_elus']}")
                        st.markdown("---")
                        for nom, score, ecart, detail in [
                            ("Genre", row["score_genre"], row["ecart_genre"], f"{row['ecart_genre']:.1f} pts d'écart élus/population locale"),
                            ("Âge",   row["score_age"],   row["ecart_age"],   f"{row['ecart_age']:.1f} ans d'écart élus/médiane locale"),
                            ("CSP",   row["score_csp"],   row["ecart_csp"],   f"{row['ecart_csp']:.1f} pts d'écart sur % cadres locaux"),
                        ]:
                            e = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
                            st.markdown(f"{e} **{nom}** — {score:.0f}/100  \n<small style='color:#888'>{detail}</small>", unsafe_allow_html=True)
                            st.progress(int(score) / 100)

                    with col2:
                        st.markdown("#### 🇫🇷 IRD national")
                        st.caption("Comparaison aux références françaises")
                        st.markdown(f"**Score : {ird_nat_val}/100**")
                        st.progress(int(ird_nat_val) / 100)
                        st.markdown(f"Rang national : **{row['rang_nat']:,}/{nb_communes:,}**".replace(",", " "))
                        st.markdown(f"Références : {REF_PCT_FEMMES}% femmes | {REF_AGE_MEDIAN} ans | {REF_PCT_CADRES}% cadres")
                        st.markdown("---")
                        for nom, score, detail in [
                            ("Genre", row["score_genre_nat"], f"vs {REF_PCT_FEMMES}% femmes (France)"),
                            ("Âge",   row["score_age_nat"],   f"vs {REF_AGE_MEDIAN} ans (France)"),
                            ("CSP",   row["score_csp_nat"],   f"vs {REF_PCT_CADRES}% cadres (France)"),
                        ]:
                            e = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
                            st.markdown(f"{e} **{nom}** — {score:.0f}/100  \n<small style='color:#888'>{detail}</small>", unsafe_allow_html=True)
                            st.progress(int(score) / 100)

                        # Radar chart IRD national
                        categories = ["Genre", "Âge", "CSP"]
                        values = [row["score_genre_nat"], row["score_age_nat"], row["score_csp_nat"]]
                        fig_radar = go.Figure(data=go.Scatterpolar(
                            r=values + [values[0]],
                            theta=categories + [categories[0]],
                            fill="toself", fillcolor=couleur, opacity=0.3,
                            line=dict(color=couleur, width=2),
                            name=row["commune"],
                        ))
                        fig_radar.add_trace(go.Scatterpolar(
                            r=[100, 100, 100, 100],
                            theta=categories + [categories[0]],
                            fill="toself", fillcolor="rgba(200,200,200,0.1)",
                            line=dict(color="gray", dash="dot", width=1),
                            name="Max", showlegend=False,
                        ))
                        fig_radar.update_layout(
                            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                            showlegend=False, height=260,
                            margin=dict(l=20, r=20, t=30, b=20),
                        )
                        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("Entrez au moins 2 caractères pour rechercher une commune.")

afficher_footer()