"""
pages/5_Diversite.py
--------------------
Maires issus de l'immigration — élections municipales 2026
Données issues de sources journalistiques publiques (AJ+, France Info, Wikipedia)
"""

import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Diversité", page_icon="🌍", layout="wide")

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

st.title("🌍 Diversité & Représentation")
st.markdown(
    """
    La France ne collecte pas de statistiques ethniques — c'est un principe constitutionnel.
    Il est donc **impossible de mesurer officiellement** la représentation des personnes
    issues de l'immigration parmi les élus.

    Cette page s'appuie sur des **sources journalistiques publiques** (France Info, AJ+, Wikipedia,
    presse locale) pour documenter un phénomène notable des élections municipales 2026 :
    l'émergence visible de maires issus de l'immigration ou ayant des liens biographiques
    avec l'Afrique subsaharienne ou le Maghreb.

    > ⚠️ *Ces données sont déclaratives et issues de la presse. Elles ne constituent pas
    une statistique officielle. La mention de l'origine est faite dans un esprit
    de documentation factuelle, non de catégorisation.*
    """
)

# ─────────────────────────────────────────────────────────────────────────────
# DONNÉES — issues de sources journalistiques publiques
# ─────────────────────────────────────────────────────────────────────────────

maires_diversite = pd.DataFrame([
    # Élus au 1er tour — liens avec Afrique subsaharienne
    {
        "Prénom Nom"       : "Leslie Halleur Echaroux",
        "Commune"          : "Saint-Mammès",
        "Département"      : "Seine-et-Marne (77)",
        "Code_dep"         : "77",
        "Tour"             : "1er tour",
        "Parti"            : "Sans étiquette",
        "Score (%)"        : None,
        "Origine (presse)" : "Cameroun",
        "Profil"           : "Élue sans étiquette",
        "lat"              : 48.376, "lon": 2.810,
    },
    {
        "Prénom Nom"       : "Bally Bagayoko",
        "Commune"          : "Saint-Denis",
        "Département"      : "Seine-Saint-Denis (93)",
        "Code_dep"         : "93",
        "Tour"             : "1er tour",
        "Parti"            : "LFI-PCF",
        "Score (%)"        : 50.77,
        "Origine (presse)" : "Mali",
        "Profil"           : "52 ans, ancien basketteur, cadre RATP, adjoint depuis 2001. "
                             "1ère ville de +100 000 hab. remportée par LFI.",
        "lat"              : 48.936, "lon": 2.358,
    },
    {
        "Prénom Nom"       : "Yahaya Soukouna",
        "Commune"          : "Fleury-Mérogis",
        "Département"      : "Essonne (91)",
        "Code_dep"         : "91",
        "Tour"             : "1er tour",
        "Parti"            : "Divers gauche",
        "Score (%)"        : 50.71,
        "Origine (presse)" : "Mali (soninké)",
        "Profil"           : "35 ans, enfant de Fleury-Mérogis, éducateur sportif, "
                             "diplômé Bac+5 ENDC. Élu avec seulement 30 voix d'avance.",
        "lat"              : 48.630, "lon": 2.364,
    },
    {
        "Prénom Nom"       : "Marieme Tamata-Varin-Watt",
        "Commune"          : "Yebles",
        "Département"      : "Seine-et-Marne (77)",
        "Code_dep"         : "77",
        "Tour"             : "1er tour",
        "Parti"            : "Sans étiquette",
        "Score (%)"        : None,
        "Origine (presse)" : "Mauritanie",
        "Profil"           : "Élue sans étiquette",
        "lat"              : 48.558, "lon": 2.731,
    },
    {
        "Prénom Nom"       : "Mohamed Gnabaly",
        "Commune"          : "L'Île-Saint-Denis",
        "Département"      : "Seine-Saint-Denis (93)",
        "Code_dep"         : "93",
        "Tour"             : "1er tour",
        "Parti"            : "Les Écologistes",
        "Score (%)"        : None,
        "Origine (presse)" : "Sénégal",
        "Profil"           : "Élu écologiste",
        "lat"              : 48.935, "lon": 2.333,
    },
    {
        "Prénom Nom"       : "Kwami Agbegna",
        "Commune"          : "Provin",
        "Département"      : "Nord (59)",
        "Code_dep"         : "59",
        "Tour"             : "1er tour",
        "Parti"            : "Divers droite",
        "Score (%)"        : None,
        "Origine (presse)" : "Togo",
        "Profil"           : "Élu divers droite",
        "lat"              : 50.507, "lon": 3.089,
    },
    # Élus au 2e tour
    {
        "Prénom Nom"       : "Aly Diouara",
        "Commune"          : "La Courneuve",
        "Département"      : "Seine-Saint-Denis (93)",
        "Code_dep"         : "93",
        "Tour"             : "2e tour",
        "Parti"            : "LFI",
        "Score (%)"        : 51.53,
        "Origine (presse)" : "Franco-gambien",
        "Profil"           : "Responsable associatif et fonctionnaire territorial. "
                             "A fusionné sa liste avec celle de Nadia Chahboune (PCF).",
        "lat"              : 48.930, "lon": 2.393,
    },
    {
        "Prénom Nom"       : "Mehdi Nezzar",
        "Commune"          : "Le Bourget",
        "Département"      : "Seine-Saint-Denis (93)",
        "Code_dep"         : "93",
        "Tour"             : "2e tour",
        "Parti"            : "Divers gauche",
        "Score (%)"        : 52.04,
        "Origine (presse)" : "Maghreb (présumé, presse locale)",
        "Profil"           : "Ex directeur des Sports et de la Jeunesse de la ville.",
        "lat"              : 48.934, "lon": 2.426,
    },
    {
        "Prénom Nom"       : "Demba Traoré",
        "Commune"          : "Le Blanc-Mesnil",
        "Département"      : "Seine-Saint-Denis (93)",
        "Code_dep"         : "93",
        "Tour"             : "2e tour",
        "Parti"            : "Divers gauche",
        "Score (%)"        : 51.49,
        "Origine (presse)" : "Afrique subsaharienne (présumé, presse)",
        "Profil"           : "S'est imposé face au sénateur et ancien maire Thierry Meignen.",
        "lat"              : 48.940, "lon": 2.461,
    },
    {
        "Prénom Nom"       : "Mélissa Youssouf",
        "Commune"          : "Villepinte",
        "Département"      : "Seine-Saint-Denis (93)",
        "Code_dep"         : "93",
        "Tour"             : "2e tour",
        "Parti"            : "Union de la gauche",
        "Score (%)"        : 66.76,
        "Origine (presse)" : "Comores",
        "Profil"           : "Vice-présidente du conseil départemental de Seine-Saint-Denis. "
                             "Victoire très large avec 66,76% des voix.",
        "lat"              : 48.962, "lon": 2.546,
    },
    {
        "Prénom Nom"       : "Sonia Benameur",
        "Commune"          : "Ris-Orangis",
        "Département"      : "Essonne (91)",
        "Code_dep"         : "91",
        "Tour"             : "2e tour",
        "Parti"            : "Divers droite",
        "Score (%)"        : 49.44,
        "Origine (presse)" : "Maghreb (présumé, presse)",
        "Profil"           : "26 ans — la plus jeune. Ancienne attachée parlementaire. "
                             "Ville de plus de 30 000 habitants.",
        "lat"              : 48.651, "lon": 2.416,
    },
    {
        "Prénom Nom"       : "Bassi Konaté",
        "Commune"          : "Sarcelles",
        "Département"      : "Val-d'Oise (95)",
        "Code_dep"         : "95",
        "Tour"             : "2e tour",
        "Parti"            : "Liste civique / LFI",
        "Score (%)"        : 55.0,
        "Origine (presse)" : "Non confirmée explicitement",
        "Profil"           : "Ancien responsable d'un centre social de la ville.",
        "lat"              : 49.000, "lon": 2.380,
    },
    {
        "Prénom Nom"       : "Adama Gaye",
        "Commune"          : "Mantes-la-Jolie",
        "Département"      : "Yvelines (78)",
        "Code_dep"         : "78",
        "Tour"             : "2e tour",
        "Parti"            : "Sans étiquette",
        "Score (%)"        : 54.0,
        "Origine (presse)" : "Mère sénégalaise, père mauritanien",
        "Profil"           : "Cadre supérieur, porté par la jeunesse de la ville. "
                             "A battu le maire sortant en place depuis 2017.",
        "lat"              : 48.990, "lon": 1.717,
    },
    {
        "Prénom Nom"       : "Abdelkader Lahmar",
        "Commune"          : "Vaulx-en-Velin",
        "Département"      : "Métropole de Lyon (69)",
        "Code_dep"         : "69",
        "Tour"             : "2e tour",
        "Parti"            : "LFI",
        "Score (%)"        : None,
        "Origine (presse)" : "Maghreb (présumé, presse)",
        "Profil"           : "Député LFI. L'emporte avec seulement 104 voix d'avance.",
        "lat"              : 45.778, "lon": 4.919,
    },
    {
        "Prénom Nom"       : "Idir Boumertit",
        "Commune"          : "Vénissieux",
        "Département"      : "Métropole de Lyon (69)",
        "Code_dep"         : "69",
        "Tour"             : "2e tour",
        "Parti"            : "LFI",
        "Score (%)"        : None,
        "Origine (presse)" : "Maghreb (présumé, presse)",
        "Profil"           : "Député LFI. Devance la maire sortante Michèle Picard "
                             "avec seulement 25 voix d'écart.",
        "lat"              : 45.697, "lon": 4.886,
    },
])

# ─────────────────────────────────────────────────────────────────────────────
# ONGLETS
# ─────────────────────────────────────────────────────────────────────────────

tab1, tab2, tab3 = st.tabs(["Portraits", "Carte", "Contexte"])

# ══════════════════════════════════════════════════════
# TAB 1 — Portraits des maires
# ══════════════════════════════════════════════════════
with tab1:
    st.markdown("### Une nouvelle génération de maires")
    st.markdown(
        f"À l'occasion des élections municipales des 15 et 22 mars 2026, **{len(maires_diversite)} maires** "
        f"ayant des liens biographiques publics avec l'immigration ont été élus ou réélus, "
        f"selon les sources journalistiques consultées. "
        f"**{len(maires_diversite[maires_diversite['Tour'] == '1er tour'])}** l'ont été dès le premier tour."
    )

    # Filtre par tour
    filtre = st.radio("Filtrer par :", ["Tous", "1er tour", "2e tour"], horizontal=True)
    df_affiche = maires_diversite if filtre == "Tous" else maires_diversite[maires_diversite["Tour"] == filtre]

    # Affichage en cartes
    for _, row in df_affiche.iterrows():
        with st.expander(f"{'🥇' if row['Tour'] == '1er tour' else '🥈'} **{row['Prénom Nom']}** — {row['Commune']} ({row['Département']})"):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**Parti :** {row['Parti']}")
                st.markdown(f"**Tour :** {row['Tour']}")
                if row['Score (%)']:
                    st.markdown(f"**Score :** {row['Score (%)']}%")
                st.markdown(f"**Origine (presse) :** {row['Origine (presse)']}")
            with col2:
                if row['Profil']:
                    st.markdown(f"*{row['Profil']}*")

    st.markdown("---")
    st.markdown("### Tableau complet")
    cols_affichage = ["Prénom Nom", "Commune", "Département", "Tour", "Parti", "Score (%)", "Origine (presse)"]
    st.dataframe(
        df_affiche[cols_affichage].reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )


# ══════════════════════════════════════════════════════
# TAB 2 — Carte
# ══════════════════════════════════════════════════════
with tab2:
    st.markdown("### Localisation des communes concernées")

    import plotly.graph_objects as go

    fig = go.Figure()

    couleurs = {"1er tour": "#2a9d8f", "2e tour": "#e76f51"}

    for tour, groupe in maires_diversite.groupby("Tour"):
        fig.add_trace(go.Scattergeo(
            lat=groupe["lat"],
            lon=groupe["lon"],
            mode="markers+text",
            name=tour,
            marker=dict(
                size=12,
                color=couleurs[tour],
                symbol="circle",
                line=dict(width=1, color="white"),
            ),
            text=groupe["Commune"],
            textposition="top center",
            hovertemplate=(
                "<b>%{text}</b><br>"
                + groupe["Prénom Nom"].values[0] + "<br>"
                + "<extra></extra>"
            ),
            customdata=groupe[["Prénom Nom", "Parti", "Score (%)"]].values,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Maire : %{customdata[0]}<br>"
                "Parti : %{customdata[1]}<br>"
                "Score : %{customdata[2]}%<br>"
                "<extra></extra>"
            ),
        ))

    fig.update_layout(
        title="Communes avec un maire ayant des liens biographiques publics avec l'immigration",
        geo=dict(
            scope="europe",
            center=dict(lat=46.8, lon=2.3),
            projection_scale=6,
            showland=True,
            landcolor="#f5f5f5",
            showcoastlines=True,
            coastlinecolor="#cccccc",
            showframe=False,
        ),
        legend=dict(title="Tour d'élection"),
        height=600,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Coordonnées approximatives. Sources : France Info, AJ+, Wikipedia, presse locale."
    )


# ══════════════════════════════════════════════════════
# TAB 3 — Contexte
# ══════════════════════════════════════════════════════
with tab3:
    st.markdown("### Pourquoi la France ne mesure pas la diversité dans les données officielles")

    st.markdown(
        """
        **Le principe républicain d'indifférence à l'origine**

        La France ne collecte pas de statistiques ethniques ou raciales dans ses données
        officielles. Le Conseil constitutionnel a censuré en 2007 une disposition qui
        aurait permis de telles statistiques, considérant qu'elles étaient contraires
        au principe d'égalité. Le Répertoire National des Élus (RNE) ne contient donc
        aucune information sur l'origine des élus.

        **Ce qu'on peut mesurer dans les données officielles**

        Le RNE contient une colonne `nationalité` pour les conseillers municipaux.
        Elle indique si l'élu est de nationalité française (FR) ou étrangère — ce qui
        ne renseigne pas sur l'origine mais permet de voir combien d'élus non-français
        siègent dans les conseils municipaux (cas des ressortissants européens notamment).

        **Ce que dit la recherche**

        Quelques études ont tenté d'approcher la question par des méthodes indirectes
        (analyse des noms et prénoms, enquêtes déclaratives). Elles montrent de façon
        générale une sous-représentation des personnes issues de l'immigration dans
        les mandats électifs, en particulier aux postes de maires.

        **Ce que montrent les élections de 2026**

        Les élections municipales de mars 2026 ont vu l'émergence visible d'élus
        ayant des liens biographiques publics avec l'immigration. Ce phénomène,
        documenté par la presse (AJ+, France Info, presse locale), est particulièrement
        notable en Seine-Saint-Denis et en Île-de-France plus généralement.

        Ces élus viennent de bords politiques variés — de la gauche radicale (LFI)
        à la droite locale — ce qui suggère que le phénomène dépasse les clivages partisans.
        """
    )

    st.info(
        "**Sources utilisées pour cette page :**\n"
        "- AJ+ Français — reportage « Qui sont les nouveaux maires français issus de l'immigration ? » (mars 2026)\n"
        "- France Info — reportage sur Bally Bagayoko (Saint-Denis)\n"
        "- La Semaine de l'Île-de-France — portrait de Yahaya Soukouna (Fleury-Mérogis)\n"
        "- Wikipedia — biographies des élus cités\n"
        "- Résultats officiels — Ministère de l'Intérieur / data.gouv.fr"
    )

afficher_footer()