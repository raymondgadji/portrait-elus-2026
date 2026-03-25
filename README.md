# 🗳️ Portrait des Élus Municipaux 2026

Dashboard interactif analysant le profil des élu·es municipaux français issus des élections des 15 et 22 mars 2026.

Réalisé dans le cadre du **Challenge Open Data data.gouv.fr** — Défi 2 : Profil des élus.

🏷️ Mot-clé challenge : `defi-municipales-2026-résultats`

## 🚀 Voir l'application

👉 [Lien Streamlit Cloud à venir]

## 📊 Ce que montre l'app

- **Parité** : répartition femmes/hommes parmi les maires et conseillers, par région et département
- **Âge** : distribution des âges, comparaison avec la population générale
- **Professions** : quelles catégories socio-professionnelles sont sur- ou sous-représentées ?
- **Carte interactive** : explorer les données par territoire

## 📦 Données utilisées

- [Répertoire National des Élus (RNE)](https://www.data.gouv.fr/datasets/repertoire-national-des-elus-1) — Ministère de l'Intérieur
- Licence : Licence Ouverte / Open Licence 2.0

## ⚙️ Installation locale

```bash
git clone https://github.com/raymondgadji/portrait-elus-2026
cd portrait-elus-2026
pip install -r requirements.txt

# Télécharger les données (voir claude.md pour les URLs)
# Placer maires.csv et conseillers.csv dans data/raw/

streamlit run app.py
```

## 👤 Auteur

Projet réalisé par [AI Raymond Gadji] — aspirant data analyst