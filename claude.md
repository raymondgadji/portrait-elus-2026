# 🗳️ claude.md — Portrait des Élus Municipaux 2026
> Document de référence du projet — à lire à chaque nouvelle session avec Claude

---

## 👤 Profil développeur

- **Nom** : Raymond Gadji
- **Profil LinkedIn** : https://www.linkedin.com/in/raymond-gadji/
- **Formation** : Bootcamp Data Analyst, Simplon Paris Montreuil
- **Stack maîtrisée** : Python (intermédiaire), Streamlit, Pandas, Plotly, HTML/CSS/JS vanilla, Flask (débutant)
- **Projets existants** :
  - [Trajets Verts Paris](https://trajets-verts-paris.streamlit.app/)
  - [Éléphants mini-RAG](https://elephants.streamlit.app/)
- **Environnement** : VS Code local (Windows) + déploiement Streamlit Cloud
- **Repo GitHub** : https://github.com/raymondgadji/portrait-elus-2026

---

## 🎯 Objectif du projet

Participer au **Défi 2 — "Profil des élus"** du Challenge Open Data data.gouv.fr.
- **Deadline** : 13 avril 2026
- **Mot-clé publié** : `defi-municipales-2026-resultats`
- **URL défi** : https://defis.data.gouv.fr/defis/elections-municipales-2026-profils-des-elus
- **URL app** : https://portrait-elus-2026.streamlit.app
- **URL data.gouv.fr** : https://data.gouv.fr/reuses/portrait-des-elus-municipaux-2026

---

## ✅ État du projet au 1er avril 2026 — TERMINÉ

### Pages déployées et fonctionnelles
| Fichier | Page | Statut |
|---------|------|--------|
| `app.py` | Accueil + KPIs + footer | ✅ |
| `pages/1_IRD.py` | Indice de Représentativité Démocratique | ✅ |
| `pages/2_parite.py` | Parité H/F | ✅ |
| `pages/3_age.py` | Âge des élus | ✅ |
| `pages/4_diversite.py` | Diversité & représentation | ✅ |
| `pages/5_carte.py` | Carte interactive + choroplèthe IRD | ✅ |
| `pages/6_professions.py` | CSP des élus | ✅ |

### Données
- **Maires** : 34 874 lignes (`elus-maires-mai.csv`)
- **Conseillers** : 485 827 lignes (`elus-conseillers-municipaux-cm.csv`)
- **Encodage** : latin-1 (correction double-encodage dans loader.py)
- **Téléchargement** : automatique depuis data.gouv.fr au premier lancement

### Bugs résolus (historique complet)
- `KeyError: 'code_dep'` → renommage par position dans loader.py
- `OverflowError: Overflow in int64 addition` → calcul âge en Python pur
- `UnicodeEncodeError` sur Windows → suppression emojis dans explore_data.py
- `SyntaxError: keyword argument repeated: hovertemplate` → doublon supprimé
- `nan%` sur scores None → remplacement par "non disponible" / "N/D"
- Import circulaire `loader.py` → ligne erronée supprimée
- Boxplot IRD : une seule boîte → corrigé en utilisant `conseillers` comme proxy de taille
- Scatter IRD : deux colonnes verticales (0%/100%) → corrigé en utilisant `conseillers` pour le % femmes
- `with tab3:` manquant → bloc TAB3 réencapsulé correctement
- Variable morte `couleur_jauge` → supprimée
- Footer absent sur `app.py` → `afficher_footer()` ajouté en fin de fichier
- `charger_geojson()` disparue de `5_carte.py` → réintégrée
- Double `labels=` dans `px.choropleth` → supprimé

---

## 📦 Sources de données

### RNE — Répertoire National des Élus
- **URL dataset** : https://www.data.gouv.fr/datasets/repertoire-national-des-elus-1
- **Maires** : `https://www.data.gouv.fr/api/1/datasets/r/2876a346-d50c-4911-934e-19ee07b0e503`
- **Conseillers** : `https://www.data.gouv.fr/api/1/datasets/r/d5f400de-ae3f-4966-8cb6-a85c70c6c24a`
- **Séparateur** : `;` | **Encodage** : `latin-1`
- **Colonnes** : renommées par index (0→code_dep, 1→dep, ... 8→sexe, 9→date_naissance, 11→csp)

### Résultats officiels municipales 2026
- **Ministère de l'Intérieur** : https://www.resultats-elections.interieur.gouv.fr/municipales2026/

### Page Diversité — sources journalistiques
- AJ+ Français — reportage maires issus de l'immigration (mars 2026)
- France Info — Bally Bagayoko (Saint-Denis)
- La Semaine de l'Île-de-France — Yahaya Soukouna (Fleury-Mérogis)
- Résultats officiels Ministère de l'Intérieur

---

## 🗂️ Structure du projet

```
portrait-elus-2026/
├── claude.md
├── IRD.md
├── README.md
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml
├── app.py
├── data/
│   ├── raw/          ← gitignorés, téléchargés au lancement
│   └── processed/
├── pages/
│   ├── 1_IRD.py
│   ├── 2_parite.py
│   ├── 3_age.py
│   ├── 4_diversite.py
│   ├── 5_carte.py
│   └── 6_professions.py
└── utils/
    ├── __init__.py
    └── loader.py
```

---

## ⚙️ Points techniques importants

### loader.py
- Téléchargement automatique si CSV absent (`_assurer_presence`)
- Renommage par **position** (pas par nom) pour éviter les bugs d'encodage
- Correction double-encodage : `.encode("latin-1").decode("utf-8")`
- Calcul âge en Python pur (`date.today() - date(a, m, j)`) — compatible Python 3.13+
- `@st.cache_data` sur les deux fonctions de chargement
- **Ne jamais ajouter d'import dans loader.py** — risque d'import circulaire

### 1_IRD.py
- Importe `charger_maires` ET `charger_conseillers` depuis `utils.loader`
- `conseillers` chargé au niveau module (pas dans une fonction)
- Filtre `ird_df[ird_df["IRD"] >= 10]` appliqué après calcul IRD
- `nb_communes` recalculé après le filtre
- Boxplot TAB3 : utilise `conseillers` pour proxy taille (nb_conseillers par commune)
- Scatter TAB3 : utilise `conseillers` pour % femmes (valeurs continues 0-100%)
- TAB4 "Ma commune" : phrase auto + jauges visuelles + radar chart

### 5_carte.py
- Importe `charger_maires` ET `charger_conseillers`
- IRD en premier dans le selectbox — indicateur mis en avant
- Palette rouge → jaune → vert cohérente avec la page IRD
- `charger_geojson()` doit rester définie dans le fichier (ne pas la supprimer)
- Un seul bloc `labels=` dans `px.choropleth` (doublon = SyntaxError)
- `ird_dep` inclus dans le rename du tableau récapitulatif

### app.py
- Ordre navbar : IRD / Parité / Âge / Diversité / Carte / Professions
- `afficher_footer()` appelée en toute fin de fichier

### Windows / PowerShell
- La commande `rename` n'existe pas → utiliser `Rename-Item`
- Git : toujours préciser le chemin complet `pages/5_carte.py` pas juste `5_carte.py`
- Redirection `> fichier.txt` fonctionne mais nécessite `sys.stdout.reconfigure(encoding="utf-8")`

---

## 🏛️ IRD — Indice de Représentativité Démocratique

**Concept** : score synthétique par commune mesurant à quel point les élus ressemblent à leurs administrés.

### Formule
| Composante | Mesure | Poids |
|-----------|--------|-------|
| Genre | \|% femmes élues − % femmes population\| | 40% |
| Âge | \|âge moyen élus − âge médian population\| / 30 × 100 | 35% |
| CSP | \|% cadres élus − % cadres actifs INSEE\| | 25% |

- Chaque écart → score 0-100 (100 = pas d'écart, 0 = écart maximal)
- IRD = moyenne pondérée des 3 scores

### Résultats nationaux (mars 2026)
- **34 735 communes** analysées
- **IRD moyen : 45.0/100** — représentativité moyenne
- **IRD médian : 44.5/100**
- **37.6%** des communes ont un IRD < 40 (faible représentativité)
- **4.0%** des communes ont un IRD ≥ 70 (bonne représentativité)
- Composante la plus déficitaire : **l'âge** (score moyen : 29.4/100)

### Sources données IRD
- Profil élus : RNE (Ministère de l'Intérieur)
- Profil population : Recensement INSEE 2021
- Âge médian population : 42 ans (constante nationale)

---

## 🏁 Checklist publication data.gouv.fr

- [x] App déployée sur Streamlit Cloud
- [x] Réutilisation publiée sur data.gouv.fr
- [x] Jeu de données RNE lié
- [x] Mot-clé `defi-municipales-2026-resultats` ajouté
- [x] Image de couverture uploadée
- [x] Footer signé Raymond Gadji + LinkedIn sur toutes les pages

---

## 💬 Notes de session

- **25/03/2026** — Choix Option B (Défi 2 Profil des élus). Données RNE identifiées. Structure projet définie.
- **26/03/2026** — App complète (5 pages) déployée. Publiée sur data.gouv.fr. Tous les bugs résolus.
- **27/03/2026** — Page Diversité finalisée avec 15 maires, scores officiels, carte, contexte. Idée IRD identifiée.
- **29/03/2026** — Page IRD finalisée et déployée. Boxplot + scatter corrigés. TAB4 enrichi. IRD.md créé.
- **01/04/2026** — **PROJET TERMINÉ** :
  - Footer ajouté sur app.py
  - Carte choroplèthe IRD par département ajoutée dans 5_carte.py
  - IRD en premier dans le selectbox de la carte
  - claude.md final mis à jour

---

## 🔗 Liens utiles

- App live : https://portrait-elus-2026.streamlit.app
- data.gouv.fr : https://data.gouv.fr/reuses/portrait-des-elus-municipaux-2026
- GitHub : https://github.com/raymondgadji/portrait-elus-2026
- Défi officiel : https://defis.data.gouv.fr/defis/elections-municipales-2026-profils-des-elus
- RNE dataset : https://www.data.gouv.fr/datasets/repertoire-national-des-elus-1
- Résultats officiels : https://www.resultats-elections.interieur.gouv.fr/municipales2026/
- LinkedIn Raymond : https://www.linkedin.com/in/raymond-gadji/
