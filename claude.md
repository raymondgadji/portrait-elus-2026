# 🗳️ claude.md — Portrait des Élus Municipaux 2026
> Document de référence du projet — à lire à chaque nouvelle session avec Claude

---

## 👤 Profil développeur

- **Nom du projet** : Portrait des Élus Municipaux 2026
- **Développeur** : Aspirant data analyst, bootcamp Simplon Paris Montreuil
- **Stack maîtrisée** : Python (débutant), Streamlit, HTML/CSS/JS vanilla, Flask (débutant)
- **Projets existants** :
  - [Trajets Verts Paris](https://trajets-verts-paris.streamlit.app/)
  - [Éléphants mini-RAG](https://elephants.streamlit.app/)
- **Environnement** : VS Code local + déploiement Streamlit Cloud
- **Repo GitHub** : _(à créer — nommer : `portrait-elus-2026`)_

---

## 🎯 Objectif du projet

Participer au **Défi 2 — "Profil des élus"** du Challenge Open Data data.gouv.fr.
- Deadline : **13 avril 2026**
- Mot-clé à publier : `defi-municipales-2026-résultats`
- URL défi : https://defis.data.gouv.fr/defis/elections-municipales-2026-profils-des-elus

**Question centrale de notre app** :
> *Qui sont les élu·es municipaux de France en 2026 ? Sont-ils représentatifs de la population ?*

---

## 📦 Sources de données

### Source principale — Répertoire National des Élus (RNE)
- **Producteur** : Ministère de l'Intérieur
- **URL dataset** : https://www.data.gouv.fr/datasets/repertoire-national-des-elus-1
- **Fichier maires** (CSV ~4 Mo) :
  `https://www.data.gouv.fr/api/1/datasets/r/2876a346-d50c-4911-934e-19ee07b0e503`
- **Fichier conseillers municipaux** (CSV ~58 Mo) :
  `https://www.data.gouv.fr/api/1/datasets/r/d5f400de-ae3f-4966-8cb6-a85c70c6c24a`
- **Licence** : Licence Ouverte / Open Licence 2.0 ✅ (réutilisation libre)
- **Séparateur CSV** : point-virgule (`;`)
- **Mise à jour** : décembre 2025 (données pré-élections 2026 — les nouvelles données post-22 mars seront publiées)

### Source secondaire — Élus sortants 2026
- **URL dataset** : https://www.data.gouv.fr/datasets/elections-municipales-2026-maires-et-conseillers-municipaux-sortants
- Permet la comparaison avant/après élections

### À surveiller (données post-élections)
- Les nouvelles listes d'élus issus du scrutin des 15 et 22 mars 2026 seront publiées sur data.gouv.fr
- Surveiller : https://www.data.gouv.fr/datasets/elections-municipales-2026-resultats-du-premier-tour

---

## 🗂️ Structure du projet (arborescence cible)

```
portrait-elus-2026/
├── claude.md                  # CE FICHIER — à garder à la racine
├── README.md
├── requirements.txt
├── .gitignore
├── app.py                     # Point d'entrée Streamlit
├── data/
│   ├── raw/                   # Données brutes téléchargées (non commitées)
│   │   ├── maires.csv
│   │   └── conseillers.csv
│   └── processed/             # Données nettoyées (non commitées)
├── pages/
│   ├── 01_parité.py
│   ├── 02_âge.py
│   ├── 03_professions.py
│   └── 04_territoires.py
└── utils/
    ├── loader.py              # Chargement et cache des données
    └── charts.py              # Fonctions de visualisation réutilisables
```

---

## 🧱 Architecture de l'app Streamlit

### Page d'accueil (`app.py`)
- Titre + explication du projet
- KPIs clés : nb total d'élus, % femmes, âge moyen
- Lien vers les 4 onglets thématiques

### Page 1 — Parité hommes/femmes
- % de femmes maires par région (carte choroplèthe)
- Évolution parité si données historiques disponibles
- Top/Flop départements parité

### Page 2 — Âge des élus
- Distribution des âges (histogramme)
- Âge moyen maire vs conseiller par département
- Comparaison âge élus vs âge population INSEE

### Page 3 — Professions
- Donut chart des CSP (catégories socio-professionnelles)
- Comparaison avec la répartition nationale INSEE
- Quelles professions sur-représentées ?

### Page 4 — Carte interactive
- Carte France avec filtre par variable (genre, âge, CSP)
- Granularité : région → département → commune (si données dispo)

---

## ⚙️ Stack technique

```
Python           3.11+
Streamlit        >= 1.32
Pandas           >= 2.0
Plotly           >= 5.18       # Graphiques interactifs
Folium           >= 0.16       # Cartes (optionnel)
Geopandas        >= 0.14       # Cartes choroplèthes
Requests         >= 2.31       # Téléchargement données
```

### `requirements.txt`
```
streamlit
pandas
plotly
requests
geopandas
folium
streamlit-folium
openpyxl
```

---

## 🚀 Plan de développement (3 semaines)

### Semaine 1 — Data (25 mars → 1er avril)
- [ ] Créer le repo GitHub `portrait-elus-2026`
- [ ] Télécharger les données RNE (maires + conseillers)
- [ ] Explorer les colonnes disponibles (Jupyter ou VS Code)
- [ ] Nettoyer : valeurs manquantes, formats dates, codes département
- [ ] Calculer les KPIs de base (parité, âge moyen, top professions)

### Semaine 2 — App (1er → 8 avril)
- [ ] Créer `app.py` avec structure de navigation
- [ ] Page Parité : graphiques + carte
- [ ] Page Âge : histogramme + comparaison INSEE
- [ ] Page Professions : donut + tableau

### Semaine 3 — Finitions (8 → 13 avril)
- [ ] Page Carte interactive (Folium ou Plotly)
- [ ] Habillage CSS / thème Streamlit
- [ ] README bien rédigé
- [ ] Déploiement Streamlit Cloud
- [ ] Publication réutilisation sur data.gouv.fr avec mot-clé

---

## 📋 Colonnes attendues dans les fichiers RNE

D'après la documentation et les précédentes versions du RNE :

| Colonne | Description |
|---------|-------------|
| `Code du département` | Code INSEE département (ex: 75, 13) |
| `Libellé du département` | Nom du département |
| `Code de la commune` | Code INSEE commune |
| `Libellé de la commune` | Nom de la commune |
| `Nom de l'élu` | Nom de famille |
| `Prénom de l'élu` | Prénom |
| `Code sexe` | M ou F |
| `Date de naissance` | Format JJ/MM/AAAA |
| `Code de la catégorie socio-professionnelle` | Code CSP INSEE |
| `Libellé de la catégorie socio-professionnelle` | Libellé CSP |
| `Date de début du mandat` | |
| `Libellé de la fonction` | Maire, Adjoint, Conseiller... |

---

## 🏁 Checklist publication data.gouv.fr

- [ ] App déployée sur Streamlit Cloud
- [ ] Lien fonctionnel testé
- [ ] Compte créé sur data.gouv.fr
- [ ] Réutilisation publiée avec :
  - Titre clair
  - Description du projet
  - Jeux de données liés (RNE)
  - Mot-clé : **`defi-municipales-2026-résultats`**
  - URL de l'app Streamlit

---

## 💬 Notes de session

_Ajouter ici les décisions importantes prises au fil des sessions_

- **25/03/2026** — Choix Option B (Défi 2 Profil des élus). Données RNE identifiées. Structure projet définie.

---

## 🔗 Liens utiles

- data.gouv.fr : https://www.data.gouv.fr
- Défi officiel : https://defis.data.gouv.fr/defis/elections-municipales-2026-profils-des-elus
- RNE dataset : https://www.data.gouv.fr/datasets/repertoire-national-des-elus-1
- Guide publication réutilisation : https://guides.data.gouv.fr/publier-des-donnees/guide-data.gouv.fr/reutilisations
- Streamlit docs : https://docs.streamlit.io
- Plotly Express : https://plotly.com/python/plotly-express/
