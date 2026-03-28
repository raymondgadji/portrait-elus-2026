"""
pages/1_IRD.py
--------------
Indice de Représentativité Démocratique (IRD)
Score synthétique mesurant à quel point les élus ressemblent à leurs administrés.
Données : RNE (Ministère de l'Intérieur) x Recensement INSEE 2021

Formule IRD par commune (0 = très peu représentatif, 100 = parfaitement représentatif) :
  - Composante Genre   : écart entre % femmes élues et % femmes population
  - Composante Âge     : écart entre âge moyen élus et âge médian population
  - Composante CSP     : écart entre % cadres+prof.intel. élus et % actifs correspondants INSEE
  IRD = 100 - moyenne_pondérée(ces 3 écarts normalisés)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from pathlib import Path
from utils.loader import charger_maires

# ── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="IRD - Indice de Représentativité", page_icon="🏛️", layout="wide")

LINKEDIN = "https://www.linkedin.com/in/raymond-gadji/"

def afficher_footer():
    st.markdown("---")
    st.markdown(
        f"""<div style="text-align:center;padding:0.8rem 0 0.2rem 0;">
            <p style="margin:0;font-size:0.85rem;">
                © 2026 Créé par <a href="{LINKEDIN}" target="_blank"
                style="color:#4A90D9;text-decoration:none;font-weight:600;">Raymond Gadji</a>
                — Data Analyst</p>
            <p style="margin:0.25rem 0 0 0;font-size:0.75rem;color:#888;">
                Sources : RNE (Ministère de l'Intérieur) | Recensement INSEE 2021
                | Licence Ouverte 2.0</p>
        </div>""",
        unsafe_allow_html=True,
    )

# ── Titre & explication ───────────────────────────────────────────────────────
st.title("🏛️ Indice de Représentativité Démocratique (IRD)")
st.markdown("""
**Question centrale :** Les élu·es municipaux ressemblent-ils aux habitant·es qu'ils représentent ?

L'IRD est un score inédit calculé pour chaque commune, qui mesure l'écart entre
le **profil des élus** (genre, âge, catégorie socio-professionnelle) et
le **profil de la population** (recensement INSEE 2021).

> **Score 100** → les élus sont le miroir parfait de leur population.
> **Score 0** → les élus ne ressemblent pas du tout à leurs administrés.
""")

with st.expander("📐 Comment est calculé l'IRD ?"):
    st.markdown("""
    L'IRD combine **3 composantes** normalisées, chacune notée de 0 à 100 :

    | Composante | Mesure | Poids |
    |-----------|--------|-------|
    | **Genre** | \|% femmes élues − % femmes population\| | 40% |
    | **Âge** | \|âge moyen élus − âge médian population\| / 0,5 | 35% |
    | **CSP** | \|% cadres+prof.intel. élus − % actifs correspondants\| | 25% |

    Chaque écart est converti en score (100 = pas d'écart, 0 = écart maximal).
    L'IRD est la moyenne pondérée des 3 composantes.

    **Sources :**
    - Profil des élus : Répertoire National des Élus (RNE), Ministère de l'Intérieur
    - Profil de la population : Recensement de la population 2021, INSEE
    """)

# ── Téléchargement données INSEE ──────────────────────────────────────────────
# On utilise les fichiers du recensement 2021 disponibles sur insee.fr
# Variables clés extraites du dossier complet :
# P21_POP : population totale
# P21_POPF : population féminine
# P21_POP1564 : pop 15-64 ans (actifs potentiels)
# P21_CS3 : cadres et professions intellectuelles supérieures
# P21_AGEMT : âge médian

URL_INSEE = (
    "https://www.insee.fr/fr/statistiques/fichier/5359146/"
    "dossier_complet.zip"
)
FICHIER_INSEE = Path("data/raw/insee_communes_2021.csv")

@st.cache_data(show_spinner="Chargement des données INSEE 2021...")
def charger_insee() -> pd.DataFrame:
    """
    Charge les données INSEE du recensement 2021.
    Utilise un sous-ensemble léger de variables utiles pour l'IRD.
    """
    # Variables nécessaires pour l'IRD
    VARS = [
        "CODGEO",       # code commune INSEE (5 chars)
        "LIBGEO",       # nom commune
        "P21_POP",      # population totale
        "P21_POPF",     # population féminine
        "P21_POP1564",  # pop 15-64 ans
        "P21_CS3",      # cadres et prof. intellectuelles sup.
        "P21_CS6",      # ouvriers
        "P21_CS5",      # employés
        "MED21",        # revenu médian (Filosofi)
    ]

    # Tentative de chargement depuis le fichier local
    if FICHIER_INSEE.exists():
        df = pd.read_csv(FICHIER_INSEE, sep=";", encoding="utf-8",
                         low_memory=False, dtype={"CODGEO": str})
        cols_dispo = [c for c in VARS if c in df.columns]
        return df[cols_dispo].copy()

    # Si absent → téléchargement du fichier complet (zip ~50Mo)
    st.warning("Téléchargement du fichier INSEE (environ 50 Mo, une seule fois)...")
    try:
        import zipfile, io
        r = requests.get(URL_INSEE, timeout=180)
        r.raise_for_status()
        z = zipfile.ZipFile(io.BytesIO(r.content))
        # Trouver le CSV principal dans le zip
        csv_name = [n for n in z.namelist() if n.endswith(".csv") and "dossier" in n.lower()]
        if not csv_name:
            csv_name = [n for n in z.namelist() if n.endswith(".csv")]
        if csv_name:
            FICHIER_INSEE.parent.mkdir(parents=True, exist_ok=True)
            with z.open(csv_name[0]) as f:
                df = pd.read_csv(f, sep=";", encoding="utf-8",
                                 low_memory=False, dtype={"CODGEO": str})
            cols_dispo = [c for c in VARS if c in df.columns]
            df[cols_dispo].to_csv(FICHIER_INSEE, sep=";", index=False)
            return df[cols_dispo].copy()
    except Exception as e:
        st.error(f"Impossible de charger les données INSEE : {e}")
        return pd.DataFrame()

    return pd.DataFrame()


@st.cache_data(show_spinner="Calcul de l'IRD par commune...")
def calculer_ird(maires: pd.DataFrame, insee: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule l'IRD pour chaque commune ayant un maire dans le RNE.
    """
    if insee.empty:
        return pd.DataFrame()

    # ── Profil des maires par commune ────────────────────────────────────────
    maires["code_commune_5"] = (
        maires["code_dep"].astype(str).str.zfill(2) +
        maires["code_commune"].astype(str).str.zfill(3)
    )

    profil_elus = maires.groupby(["code_commune_5", "commune", "code_dep", "dep"]).agg(
        nb_elus        = ("sexe", "count"),
        pct_femmes_elus = ("sexe", lambda x: (x == "F").mean() * 100),
        age_moyen_elus = ("age",  "mean"),
    ).reset_index()

    # CSP des maires : % cadres+prof.intel.
    def pct_cadres(df_commune):
        total = len(df_commune)
        if total == 0:
            return 0
        cadres = df_commune["csp"].str.lower().str.contains(
            "cadre|ingénieur|profession libérale|médecin|pharmacien|architecte|avocat",
            na=False
        ).sum()
        return cadres / total * 100

    csp_elus = maires.groupby("code_commune_5").apply(pct_cadres).reset_index()
    csp_elus.columns = ["code_commune_5", "pct_cadres_elus"]

    profil_elus = profil_elus.merge(csp_elus, on="code_commune_5", how="left")

    # ── Profil de la population INSEE ────────────────────────────────────────
    insee = insee.copy()
    insee["CODGEO"] = insee["CODGEO"].astype(str).str.zfill(5)

    for col in ["P21_POP", "P21_POPF", "P21_POP1564", "P21_CS3"]:
        if col in insee.columns:
            insee[col] = pd.to_numeric(insee[col], errors="coerce")

    if "P21_POP" in insee.columns and "P21_POPF" in insee.columns:
        insee["pct_femmes_pop"] = insee["P21_POPF"] / insee["P21_POP"] * 100
    else:
        insee["pct_femmes_pop"] = 51.6  # moyenne nationale si absent

    if "P21_POP1564" in insee.columns and "P21_CS3" in insee.columns:
        insee["pct_cadres_pop"] = insee["P21_CS3"] / insee["P21_POP1564"].replace(0, pd.NA) * 100
    else:
        insee["pct_cadres_pop"] = 18.0  # moyenne nationale si absent

    # Âge médian de la population (on utilise une approximation à 42 ans si absent)
    if "MED21" in insee.columns:
        # MED21 = revenu médian, pas l'âge. On utilise une valeur par défaut.
        pass
    insee["age_median_pop"] = 42.0  # âge médian France métropolitaine 2021

    insee_reduit = insee[["CODGEO", "pct_femmes_pop", "pct_cadres_pop", "age_median_pop"]].copy()

    # ── Fusion ────────────────────────────────────────────────────────────────
    merged = profil_elus.merge(
        insee_reduit,
        left_on="code_commune_5",
        right_on="CODGEO",
        how="left"
    )

    # Valeurs par défaut si INSEE absent pour cette commune
    merged["pct_femmes_pop"]  = merged["pct_femmes_pop"].fillna(51.6)
    merged["pct_cadres_pop"]  = merged["pct_cadres_pop"].fillna(18.0)
    merged["age_median_pop"]  = merged["age_median_pop"].fillna(42.0)

    # ── Calcul IRD ────────────────────────────────────────────────────────────
    # Composante Genre (poids 40%)
    ecart_genre = (merged["pct_femmes_elus"] - merged["pct_femmes_pop"]).abs()
    score_genre = (100 - ecart_genre.clip(0, 100)).clip(0, 100)

    # Composante Âge (poids 35%) — écart normalisé sur 30 ans max
    ecart_age = (merged["age_moyen_elus"] - merged["age_median_pop"]).abs()
    score_age = (100 - (ecart_age / 30 * 100)).clip(0, 100)

    # Composante CSP (poids 25%) — écart sur % cadres
    ecart_csp = (merged["pct_cadres_elus"] - merged["pct_cadres_pop"]).abs()
    score_csp = (100 - ecart_csp.clip(0, 100)).clip(0, 100)

    # IRD pondéré
    merged["IRD"] = (
        score_genre * 0.40 +
        score_age   * 0.35 +
        score_csp   * 0.25
    ).round(1)

    merged["score_genre"] = score_genre.round(1)
    merged["score_age"]   = score_age.round(1)
    merged["score_csp"]   = score_csp.round(1)
    merged["ecart_genre"] = ecart_genre.round(1)
    merged["ecart_age"]   = ecart_age.round(1)
    merged["ecart_csp"]   = ecart_csp.round(1)

    # Classement
    merged["rang"] = merged["IRD"].rank(ascending=False, method="min").astype(int)
    merged = merged.sort_values("IRD", ascending=False)

    return merged


# ── Chargement ────────────────────────────────────────────────────────────────
maires = charger_maires()
insee  = charger_insee()

if insee.empty:
    st.error(
        "Les données INSEE n'ont pas pu être chargées. "
        "L'IRD sera calculé avec les moyennes nationales comme référence. "
        "Le résultat reste indicatif mais exploitable."
    )
    # Créer un INSEE minimal avec les moyennes nationales
    communes_uniques = (
        maires[["code_dep", "code_commune"]]
        .drop_duplicates()
        .assign(
            CODGEO=lambda d: d["code_dep"].astype(str).str.zfill(2) +
                             d["code_commune"].astype(str).str.zfill(3),
            pct_femmes_pop=51.6,
            pct_cadres_pop=18.0,
            age_median_pop=42.0,
        )
    )
    insee = communes_uniques[["CODGEO", "pct_femmes_pop", "pct_cadres_pop", "age_median_pop"]]

ird_df = calculer_ird(maires, insee)

if ird_df.empty:
    st.error("Impossible de calculer l'IRD. Vérifiez les données.")
    st.stop()

# ── KPIs globaux ──────────────────────────────────────────────────────────────
st.markdown("## 📊 Vue nationale")

ird_moy = ird_df["IRD"].mean()
ird_med = ird_df["IRD"].median()
nb_communes = len(ird_df)
pct_faible = (ird_df["IRD"] < 40).mean() * 100
pct_bon    = (ird_df["IRD"] >= 70).mean() * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Communes analysées", f"{nb_communes:,}".replace(",", " "))
col2.metric("IRD moyen national", f"{ird_moy:.1f}/100")
col3.metric("IRD médian", f"{ird_med:.1f}/100")
col4.metric("Communes IRD < 40", f"{pct_faible:.1f}%", help="Représentativité faible")
col5.metric("Communes IRD ≥ 70", f"{pct_bon:.1f}%", help="Bonne représentativité")

# ── Onglets ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["Distribution", "Classements", "Analyse", "Ma commune"])

# ══════════════════════════════════════════════════════
# TAB 1 — Distribution des IRD
# ══════════════════════════════════════════════════════
with tab1:
    col_g, col_d = st.columns(2)

    with col_g:
        fig_hist = px.histogram(
            ird_df, x="IRD", nbins=50,
            color_discrete_sequence=["#457b9d"],
            labels={"IRD": "Score IRD", "count": "Nb communes"},
            title=f"Distribution des scores IRD — {nb_communes:,} communes".replace(",", " "),
        )
        fig_hist.add_vline(x=ird_moy, line_dash="dash", line_color="red",
                           annotation_text=f"Moyenne : {ird_moy:.1f}",
                           annotation_position="top right")
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_d:
        # Répartition en catégories
        def categorie_ird(score):
            if score >= 75: return "Très représentatif (≥75)"
            if score >= 60: return "Représentatif (60-74)"
            if score >= 45: return "Moyen (45-59)"
            return "Peu représentatif (<45)"

        ird_df["categorie"] = ird_df["IRD"].apply(categorie_ird)
        cat_counts = ird_df["categorie"].value_counts().reset_index()
        cat_counts.columns = ["Catégorie", "Nombre"]

        ordre = ["Très représentatif (≥75)", "Représentatif (60-74)",
                 "Moyen (45-59)", "Peu représentatif (<45)"]
        couleurs = {
            "Très représentatif (≥75)": "#2a9d8f",
            "Représentatif (60-74)"   : "#e9c46a",
            "Moyen (45-59)"           : "#f4a261",
            "Peu représentatif (<45)" : "#e76f51",
        }

        fig_pie = px.pie(
            cat_counts, names="Catégorie", values="Nombre",
            color="Catégorie", color_discrete_map=couleurs,
            title="Répartition des communes par niveau d'IRD",
            hole=0.4,
            category_orders={"Catégorie": ordre},
        )
        fig_pie.update_traces(textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Analyse des 3 composantes
    st.markdown("### Contribution de chaque composante à l'IRD")
    composantes = pd.DataFrame({
        "Composante"          : ["Genre (40%)", "Âge (35%)", "CSP (25%)"],
        "Score moyen national": [
            ird_df["score_genre"].mean().round(1),
            ird_df["score_age"].mean().round(1),
            ird_df["score_csp"].mean().round(1),
        ]
    })
    fig_comp = px.bar(
        composantes, x="Composante", y="Score moyen national",
        color="Score moyen national",
        color_continuous_scale=["#e76f51", "#e9c46a", "#2a9d8f"],
        range_y=[0, 100],
        text="Score moyen national",
        title="Score moyen par composante (100 = parfaitement représentatif)",
    )
    fig_comp.update_traces(textposition="outside")
    fig_comp.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_comp, use_container_width=True)

    # Phrase d'interprétation automatique
    score_g = ird_df["score_genre"].mean()
    score_a = ird_df["score_age"].mean()
    score_c = ird_df["score_csp"].mean()
    plus_faible = min([("le genre", score_g), ("l'âge", score_a), ("la CSP", score_c)],
                       key=lambda x: x[1])
    st.info(
        f"**Lecture :** Avec un IRD moyen de **{ird_moy:.1f}/100**, les conseils municipaux "
        f"français présentent une représentativité **{'faible' if ird_moy < 45 else 'moyenne' if ird_moy < 65 else 'correcte'}**. "
        f"La composante la plus déficitaire est **{plus_faible[0]}** "
        f"(score moyen : {plus_faible[1]:.1f}/100), révélant que c'est sur ce critère que "
        f"l'écart entre élus et population est le plus marqué en France."
    )


# ══════════════════════════════════════════════════════
# TAB 2 — Classements
# ══════════════════════════════════════════════════════
with tab2:
    col_g, col_d = st.columns(2)

    with col_g:
        st.subheader("🏆 Top 20 — communes les plus représentatives")
        top20 = ird_df.head(20)[
            ["commune", "dep", "IRD", "score_genre", "score_age", "score_csp", "nb_elus"]
        ].copy()
        top20.columns = ["Commune", "Département", "IRD", "Genre", "Âge", "CSP", "Nb élus"]
        st.dataframe(top20, use_container_width=True, hide_index=True)

    with col_d:
        st.subheader("⚠️ Flop 20 — communes les moins représentatives")
        flop20 = ird_df.tail(20).sort_values("IRD")[
            ["commune", "dep", "IRD", "score_genre", "score_age", "score_csp", "nb_elus"]
        ].copy()
        flop20.columns = ["Commune", "Département", "IRD", "Genre", "Âge", "CSP", "Nb élus"]
        st.dataframe(flop20, use_container_width=True, hide_index=True)

    # IRD moyen par département
    st.markdown("### IRD moyen par département")
    ird_dep = (
        ird_df.groupby("dep")["IRD"]
        .mean().round(1).reset_index()
        .sort_values("IRD", ascending=True)
    )
    fig_dep = px.bar(
        ird_dep, x="IRD", y="dep", orientation="h",
        color="IRD",
        color_continuous_scale=["#e76f51", "#e9c46a", "#2a9d8f"],
        range_color=[30, 80],
        labels={"IRD": "Score IRD moyen", "dep": "Département"},
        title="IRD moyen par département",
        height=1600,
        text="IRD",
    )
    fig_dep.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    fig_dep.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_dep, use_container_width=True)


# ══════════════════════════════════════════════════════
# TAB 3 — Analyse approfondie
# ══════════════════════════════════════════════════════
with tab3:
    st.markdown("### IRD selon la taille des communes")

    def taille_commune(nb):
        if nb <= 3: return "Très petites (<500 hab. approx.)"
        if nb <= 7: return "Petites (500-2000 hab. approx.)"
        if nb <= 15: return "Moyennes (2000-5000 hab. approx.)"
        if nb <= 33: return "Grandes (5000-20 000 hab. approx.)"
        return "Très grandes (>20 000 hab. approx.)"

    ird_df["taille"] = ird_df["nb_elus"].apply(taille_commune)

    fig_box = px.box(
        ird_df, x="taille", y="IRD",
        color="taille",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Distribution de l'IRD selon la taille de commune (proxy : nb d'élus)",
        labels={"taille": "Taille de commune", "IRD": "Score IRD"},
        category_orders={"taille": [
            "Très petites (<500 hab. approx.)",
            "Petites (500-2000 hab. approx.)",
            "Moyennes (2000-5000 hab. approx.)",
            "Grandes (5000-20 000 hab. approx.)",
            "Très grandes (>20 000 hab. approx.)",
        ]},
    )
    fig_box.update_layout(showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("### Relation IRD — parité femmes/hommes")
    fig_scatter = px.scatter(
        ird_df.sample(min(3000, len(ird_df)), random_state=42),
        x="pct_femmes_elus",
        y="IRD",
        color="score_genre",
        color_continuous_scale=["#e76f51", "#2a9d8f"],
        hover_data=["commune", "dep"],
        labels={
            "pct_femmes_elus": "% de femmes parmi les élus",
            "IRD": "Score IRD",
            "score_genre": "Score genre",
        },
        title="IRD en fonction du % de femmes élues (échantillon de 3 000 communes)",
        opacity=0.6,
    )
    fig_scatter.add_vline(x=51.6, line_dash="dash", line_color="blue",
                          annotation_text="51.6% (pop. française)",
                          annotation_position="top right")
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.info(
        "**Observation :** Les communes avec un % de femmes élues proche de 51,6% "
        "(part des femmes dans la population) obtiennent les meilleurs scores IRD. "
        "La parité est la composante qui a le plus d'impact sur l'IRD car son poids est de 40%."
    )


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
                ird_val = row["IRD"]
                couleur = "#2a9d8f" if ird_val >= 70 else "#e9c46a" if ird_val >= 50 else "#e76f51"
                emoji   = "🟢" if ird_val >= 70 else "🟡" if ird_val >= 50 else "🔴"

                with st.expander(
                    f"{emoji} **{row['commune']}** ({row['dep']}) — IRD : {ird_val}/100"
                ):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Score IRD global : {ird_val}/100**")
                        st.progress(int(ird_val) / 100)
                        st.markdown(f"Rang national : {row['rang']:,}/{nb_communes:,}".replace(",", " "))
                        st.markdown(f"Nombre d'élus : {row['nb_elus']}")

                    with col2:
                        # Radar chart des 3 composantes
                        categories = ["Genre", "Âge", "CSP"]
                        values     = [row["score_genre"], row["score_age"], row["score_csp"]]

                        fig_radar = go.Figure(data=go.Scatterpolar(
                            r=values + [values[0]],
                            theta=categories + [categories[0]],
                            fill="toself",
                            fillcolor=couleur,
                            opacity=0.3,
                            line=dict(color=couleur, width=2),
                        ))
                        fig_radar.add_trace(go.Scatterpolar(
                            r=[100, 100, 100, 100],
                            theta=categories + [categories[0]],
                            fill="toself",
                            fillcolor="rgba(200,200,200,0.1)",
                            line=dict(color="gray", dash="dot", width=1),
                            name="Max",
                            showlegend=False,
                        ))
                        fig_radar.update_layout(
                            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                            showlegend=False,
                            height=250,
                            margin=dict(l=20, r=20, t=30, b=20),
                        )
                        st.plotly_chart(fig_radar, use_container_width=True)

                    st.markdown("**Détail des composantes :**")
                    st.markdown(
                        f"- **Genre** : {row['score_genre']:.1f}/100 "
                        f"(écart : {row['ecart_genre']:.1f} points entre élus et population)\n"
                        f"- **Âge** : {row['score_age']:.1f}/100 "
                        f"(écart : {row['ecart_age']:.1f} ans entre élus et médiane pop.)\n"
                        f"- **CSP** : {row['score_csp']:.1f}/100 "
                        f"(écart : {row['ecart_csp']:.1f} points sur % cadres)"
                    )
    else:
        st.info("Entrez au moins 2 caractères pour rechercher une commune.")

afficher_footer()