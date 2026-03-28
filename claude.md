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

## ✅ État du projet au 27 mars 2026

### Pages déployées et fonctionnelles
| Fichier | Page | Statut |
|---------|------|--------|
| `app.py` | Accueil + KPIs | ✅ |
| `pages/age.py` | Âge des élus | ✅ |
| `pages/carte.py` | Carte interactive | ✅ |
| `pages/parite.py` | Parité H/F | ✅ |
| `pages/professions.py` | CSP des élus | ✅ |
| `pages/5_Diversite.py` | Diversité & représentation | ✅ |

### Données
- **Maires** : 34 874 lignes (`elus-maires-mai.csv`)
- **Conseillers** : 485 827 lignes (`elus-conseillers-municipaux-cm.csv`)
- **Encodage** : latin-1 (correction double-encodage dans loader.py)
- **Téléchargement** : automatique depuis data.gouv.fr au premier lancement

### Bugs résolus
- `KeyError: 'code_dep'` → renommage par position dans loader.py
- `OverflowError: Overflow in int64 addition` → calcul âge en Python pur
- `UnicodeEncodeError` sur Windows → suppression emojis dans explore_data.py
- `SyntaxError: keyword argument repeated: hovertemplate` → doublon supprimé
- `nan%` sur scores None → remplacement par "non disponible" / "N/D"

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
│   ├── age.py
│   ├── carte.py
│   ├── parite.py
│   ├── professions.py
│   └── 5_Diversite.py
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

### Windows / PowerShell
- La commande `rename` n'existe pas → utiliser `Rename-Item`
- La commande `code` n'est pas dans le PATH → ouvrir les fichiers depuis VS Code directement
- Redirection `> fichier.txt` fonctionne mais nécessite `sys.stdout.reconfigure(encoding="utf-8")`

---

## 💡 Idée future — Indice de Représentativité Démocratique (IRD)

**Concept** : score synthétique par commune mesurant à quel point les élus ressemblent à leurs administrés.
- Croise : âge des élus vs pyramide INSEE, genre des élus vs % population, CSP des élus vs répartition locale
- Résultat : score 0-100 par commune, cartographiable
- **Pourquoi c'est puissant** : aucun observatoire officiel français n'a encore ce score. C'est exactement la question centrale du défi. Outil actionnable pour les politiques publiques.
- **Données nécessaires** : RNE (déjà en place) + données INSEE communales (revenus, âge, CSP)
- **À coder** : `pages/6_IRD.py` + enrichissement du loader avec données INSEE

---

## 🏁 Checklist publication data.gouv.fr

- [x] App déployée sur Streamlit Cloud
- [x] Réutilisation publiée sur data.gouv.fr
- [x] Jeu de données RNE lié
- [x] Mot-clé `defi-municipales-2026-resultats` ajouté
- [x] Image de couverture uploadée
- [x] Footer signé Raymond Gadji + LinkedIn

---

## 💬 Notes de session

- **25/03/2026** — Choix Option B (Défi 2 Profil des élus). Données RNE identifiées. Structure projet définie.
- **26/03/2026** — App complète (5 pages) déployée. Publiée sur data.gouv.fr. Tous les bugs résolus.
- **27/03/2026** — Page Diversité finalisée avec 15 maires, scores officiels, carte, contexte.
  - Scores vérifiés sur resultats-elections.interieur.gouv.fr
  - Idée IRD (Indice de Représentativité Démocratique) identifiée comme prochaine étape révolutionnaire 🚀

---

## 🔗 Liens utiles

- App live : https://portrait-elus-2026.streamlit.app
- data.gouv.fr : https://data.gouv.fr/reuses/portrait-des-elus-municipaux-2026
- GitHub : https://github.com/raymondgadji/portrait-elus-2026
- Défi officiel : https://defis.data.gouv.fr/defis/elections-municipales-2026-profils-des-elus
- RNE dataset : https://www.data.gouv.fr/datasets/repertoire-national-des-elus-1
- Résultats officiels : https://www.resultats-elections.interieur.gouv.fr/municipales2026/
- LinkedIn Raymond : https://www.linkedin.com/in/raymond-gadji/
