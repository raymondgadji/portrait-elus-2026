# 🗳️ claude.md — Portrait des Élus Municipaux 2026
> Document de référence du projet — à lire à chaque nouvelle session avec Claude

---

## 👤 Profil développeur

- **Nom** : Raymond Gadji
- **Profil LinkedIn** : https://www.linkedin.com/in/raymond-gadji/ — titre : "Data analyst _ Lauréat du Challenge Open Data data.gouv.fr 2026" ✅
- **Email pro** : contact@portrait-elus-2026.fr ✅ (redirection IONOS vers gadjiraymond7@gmail.com)
- **CV** : `CV_RAYMOND_GADJI_IRD_04_2026.pdf` — à uploader en début de session si travail sur candidatures
- **Formation** : Bootcamp Data Analyst, Simplon Paris Montreuil
- **Stack maîtrisée** : Python (intermédiaire), Streamlit, Pandas, Plotly, HTML/CSS/JS vanilla, Flask (débutant)
- **Projets existants** :
  - [Trajets Verts Paris](https://trajets-verts-paris.streamlit.app/)
  - [Éléphants mini-RAG](https://elephants.streamlit.app/)
- **Environnement** : VS Code local (Windows) + déploiement Railway (production) + Streamlit Cloud (backup)
- **Repo GitHub** : https://github.com/raymondgadji/portrait-elus-2026

---

## 🎯 Objectif du projet

Participer au **Défi 2 — "Profil des élus"** du Challenge Open Data data.gouv.fr.
- **Deadline** : 13 avril 2026
- **Mot-clé publié** : `defi-municipales-2026-resultats`
- **URL défi** : https://defis.data.gouv.fr/defis/elections-municipales-2026-profils-des-elus
- **URL app Railway** : https://portrait-elus-2026-production.up.railway.app
- **URL app domaine** : https://www.portrait-elus-2026.fr ✅ (domaine actif, SSL actif, redirection HTTP→HTTPS configurée)
- **URL app Streamlit** : https://portrait-elus-2026.streamlit.app (backup — maintenu éveillé par UptimeRobot)
- **URL réutilisation data.gouv.fr** : https://www.data.gouv.fr/reuses/portrait-des-elus-municipaux-2026

---

## 🏆 RÉSULTAT — LAURÉAT DU DÉFI 2

**Portrait des Élus Municipaux 2026 a été sélectionné par data.gouv.fr** comme l'un des projets mis en avant pour le Défi 2 — Profils des élus municipaux, dans le cadre du Challenge Open Data "Résultats des élections municipales 2026".

- **Annonce officielle data.gouv.fr** (14 avril 2026) : https://www.linkedin.com/posts/data-gouv-fr_opendata-municipales2026-donnaezespubliques-activity-7452713070923182081-n7K7
- **Réutilisation publiée** : https://www.data.gouv.fr/reuses/portrait-des-elus-municipaux-2026
- **Article LinkedIn Raymond** : https://www.linkedin.com/pulse/titre-les-%25C3%25A9lus-fran%25C3%25A7ais-vous-ressemblent-ils-vraiment-raymond-gadji-olw0e

---

## ✅ État du projet au 28 avril 2026

### Pages déployées et fonctionnelles
| Fichier | Page | Statut |
|---------|------|--------|
| `app.py` | Accueil + KPIs + footer + badge | ✅ |
| `pages/1_IRD.py` | IRD V2 — données INSEE par commune | ✅ |
| `pages/2_parite.py` | Parité H/F | ✅ |
| `pages/3_age.py` | Âge des élus | ✅ |
| `pages/4_diversite.py` | Diversité & représentation | ✅ |
| `pages/5_carte.py` | Carte interactive + choroplèthe IRD | ✅ |
| `pages/6_professions.py` | CSP des élus | ✅ |

### Données
- **Maires** : 34 874 lignes (`elus-maires-mai.csv`)
- **Conseillers** : 485 827 lignes (`elus-conseillers-municipaux-cm.csv`)
- **INSEE light** : `data/processed/insee_light.csv` — 34 824 communes, 783 Ko
- **Encodage** : latin-1 (correction double-encodage dans loader.py)
- **Note** : RNE de décembre 2025 = dernière version disponible.

### Bugs résolus (historique complet)
- `KeyError: 'code_dep'` → renommage par position dans loader.py
- `OverflowError: Overflow in int64 addition` → calcul âge en Python pur
- `UnicodeEncodeError` sur Windows → suppression emojis dans explore_data.py
- `SyntaxError: keyword argument repeated: hovertemplate` → doublon supprimé
- `nan%` sur scores None → remplacement par "non disponible" / "N/D"
- Import circulaire `loader.py` → ligne erronée supprimée
- Boxplot IRD : une seule boîte → corrigé en utilisant `conseillers` comme proxy de taille
- Scatter IRD : deux colonnes verticales → corrigé en utilisant `conseillers` pour le % femmes
- `with tab3:` manquant → bloc TAB3 réencapsulé correctement
- Variable morte `couleur_jauge` → supprimée
- Footer absent sur `app.py` → `afficher_footer()` ajouté en fin de fichier
- `charger_geojson()` disparue de `5_carte.py` → réintégrée
- Double `labels=` dans `px.choropleth` → supprimé
- `SyntaxWarning: "\|"` dans expander IRD → backslashes supprimés
- Téléchargement INSEE 50Mo trop lent → remplacé par `insee_light.csv` pré-traité (783 Ko)
- `afficher_footer()` définie avant `afficher_badge_defi()` → ordre corrigé
- App crash "Oh no." → Python 3.14.3 instable, `runtime.txt` ajouté pour forcer Python 3.12
- Colonnes INSEE `P21_*` absentes → fichier INSEE 2022, colonnes `P22_*` et `C16_*`
- `TypeError: Expected numeric dtype` sur colonnes CS → conversion `.astype(float)` explicite
- Railway : "Application failed to respond" → `Procfile` ajouté + port corrigé 8501→8080
- Railway : boucle de redirection → CNAME www corrigé de `z87uxris` vers `6jbvkazp`
- IONOS : CNAME `@` impossible → utilisation de `www` + redirection IONOS
- IONOS : redirection `portrait-elus-2026.fr` pointait vers `http://` → corrigée vers `https://www.portrait-elus-2026.fr`

---

## 📦 Sources de données

### RNE — Répertoire National des Élus
- **URL dataset** : https://www.data.gouv.fr/datasets/repertoire-national-des-elus-1
- **Maires** : `https://www.data.gouv.fr/api/1/datasets/r/2876a346-d50c-4911-934e-19ee07b0e503`
- **Conseillers** : `https://www.data.gouv.fr/api/1/datasets/r/d5f400de-ae3f-4966-8cb6-a85c70c6c24a`
- **Séparateur** : `;` | **Encodage** : `latin-1`

### INSEE — Recensement 2022
- **URL** : https://www.insee.fr/fr/statistiques/fichier/5359146/dossier_complet.zip
- **Colonnes utilisées** : `P22_POP`, `P22_POPF`, `C16_POP15P_CS1` à `CS6`
- **Fichier pré-traité** : `data/processed/insee_light.csv` (783 Ko, dans le repo GitHub)
- **Script de génération** : `scripts/prepare_insee.py`

---

## 🗂️ Structure du projet

```
portrait-elus-2026/
├── claude.md
├── IRD.md
├── README.md
├── Procfile                 ← commande démarrage Railway
├── requirements.txt
├── runtime.txt              ← force Python 3.12
├── .gitignore
├── .streamlit/
│   └── config.toml
├── app.py
├── data/
│   ├── raw/                 ← gitignorés, téléchargés au lancement
│   └── processed/
│       └── insee_light.csv  ← dans le repo, 783 Ko
├── scripts/
│   ├── prepare_insee.py
│   └── explore_insee.py
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

### Procfile (Railway)
```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false
```
- Streamlit écoute sur `$PORT` (Railway injecte la valeur automatiquement)
- CORS désactivé pour éviter les erreurs cross-origin Railway

### Déploiement Railway
- **URL Railway** : `portrait-elus-2026-production.up.railway.app`
- **Domaine custom** : `www.portrait-elus-2026.fr` ✅ (DNS validés, SSL actif)
- **Région** : europe-west4 (Europe)
- **Python** : 3.12.13
- **Plan** : Hobby (gratuit, pas de mise en veille)
- CNAME `www` → `6jbvkazp.up.railway.app`
- TXT `_railway-verify.www` → valeur Railway (vérification ownership)
- Redirection IONOS : `portrait-elus-2026.fr` → `https://www.portrait-elus-2026.fr` ✅

### UptimeRobot
- Configuré sur `https://portrait-elus-2026.streamlit.app` (backup Streamlit)
- **Rôle** : maintenir l'app Streamlit éveillée (Streamlit met en veille si inactif) — ne pas changer cette URL
- 100% uptime, ping toutes les 5 minutes

### loader.py
- **Ne jamais ajouter d'import dans loader.py** — risque d'import circulaire

### 1_IRD.py — V2
- Charge `data/processed/insee_light.csv` via `charger_insee_light()`
- Fusion par `code_commune_5` entre RNE et INSEE
- Fallback moyennes nationales si commune absente

---

## 🏛️ IRD — Résultats V2 (avril 2026)

| Indicateur | V2 (données par commune) |
|-----------|--------------------------|
| Communes analysées | 32 354 |
| IRD moyen | 49.1/100 |
| IRD médian | 49.2/100 |
| Communes IRD < 40 | 26.8% |
| Communes IRD ≥ 70 | 7.7% |
| Score genre moyen | 49.1/100 |
| Score âge moyen | 41.4/100 ← le plus déficitaire |
| Score CSP moyen | 59.9/100 |

---

## 🚀 FEUILLE DE ROUTE POST-VICTOIRE

### Positionnement
Raymond se positionne comme **entrepreneur sur ce projet** — 3 axes parallèles :
1. Visibilité médiatique
2. Opportunités professionnelles
3. Développement du produit IRD

---

### PHASE 1 — Visibilité médiatique
**Fait ✅**
- Post LinkedIn annonce victoire (214 impressions)
- data.gouv.fr a commenté le post LinkedIn
- Article LinkedIn long format publié (pointe vers `https://www.portrait-elus-2026.fr`) ✅
- Post court LinkedIn rédigé
- Nom de domaine `portrait-elus-2026.fr` acheté
- App déployée sur Railway (hébergement permanent, pas de mise en veille)
- Domaine `www.portrait-elus-2026.fr` actif ✅ (DNS + SSL + redirection HTTP→HTTPS)
- Lien mis à jour sur data.gouv.fr vers `https://www.portrait-elus-2026.fr` ✅

**À faire**
- [ ] Envoyer emails journalistes : Médiapart, Le Monde Pixels, Next, France Info Tech — *rédigés, archivés*
- [ ] Envoyer emails think tanks : Terra Nova, Montaigne, Etalab, Opendata France — *rédigés, archivés*
- [ ] Envoyer emails conférences/IEP — *rédigés, archivés*
- [ ] Envoyer emails maires ciblés (20-30 mairies, score IRD bas ou exemplaires) — *template rédigé, archivé* — trouver emails via annuaire-des-mairies.fr
- [ ] Soumettre à Regards Citoyens, DemocracyOS France
- [ ] Soumettre à Prix Opendata / Datajournalism Awards / Etalab

---

### PHASE 2 — Opportunités professionnelles
**À faire**
- [x] Mettre à jour LinkedIn : "Lauréat Challenge Open Data data.gouv.fr 2026" ✅
- [x] CV mis à jour avec projet IRD en tête ✅ (`CV_RAYMOND_GADJI_IRD_04_2026.pdf`)
- [x] Préparer pitch deck 5 slides sur l'IRD ✅ (`pitch_IRD_2026.pptx` + `pitch_recruteur_2026.pptx`)
- [ ] Envoyer emails think tanks : Terra Nova, Montaigne, Etalab, Opendata France — *rédigés, archivés*
- [ ] Envoyer emails conférences/IEP — *rédigés, archivés*

---

### PHASE 3 — Développement produit & entrepreneuriat

**Idées entrepreneuriales identifiées (27/04/2026) :**

**A — Livre "La Démocratie en Chiffres"** ← idée de Raymond, validée
- Format : livre d'analyse politique et citoyenne avec l'IRD comme fil rouge
- Titre envisagé : *"La Démocratie en Chiffres — Portrait des élus municipaux français 2026"*
- Contenu : histoires que les données révèlent (déserts de représentativité, communes exemplaires, fossé générationnel)
- Cibles : bibliothèques, IEP, Sciences Po, facultés droit/science politique, think tanks
- Production : IA génère 80% du contenu à partir des données
- Différenciation vs site web : version imprimée, référençable, achetable

**B — API IRD pour collectivités** (~500€/an par abonné)
- Les communes, préfectures, associations d'élus veulent ce score
- Accès API mis à jour automatiquement
- Revenu récurrent

**C — Observatoire IRD — marque média**
- Compte LinkedIn/Twitter dédié `@IRD_France`
- Publication hebdomadaire : score d'une commune avec commentaire
- Crée une audience, attire journalistes, construit la marque

**D — Conférences et formations**
- Positionnement : *"créateur de l'IRD, lauréat data.gouv.fr"*
- IEP, écoles de commerce, associations d'élus paient pour interventions data/démocratie

**E — Partenariat think tanks**
- Terra Nova, Institut Montaigne : publications + visibilité + revenus

**F — Version européenne de l'IRD**
- Si données disponibles au niveau européen → produit exportable

**Backlog agile — estimations (28/04/2026)**

| Piste | Difficulté | Durée estimée | Outils | Valeur |
|-------|-----------|---------------|--------|--------|
| **C — Observatoire IRD** | Facile | 1 sprint · ~1 semaine | LinkedIn / X | Visibilité rapide |
| **D — Conférences & formations** | Moyen | 2 sprints · 2–3 semaines | Pitch deck prêt ✅ | 500–2000€/intervention |
| **A — Livre "La Démocratie en Chiffres"** | Moyen | 3–4 sprints · 1–2 mois | IA + données IRD | Revenu + crédibilité |
| **E — Partenariat think tanks** | Moyen | 2–3 sprints · 1 mois | Emails archivés ✅ | Crédibilité + réseau |
| **B — API IRD pour collectivités** | Complexe | 4–6 sprints · 2–3 mois | Python + Flask + Railway | Revenu récurrent ~500€/an |
| **F — Version européenne IRD** | Complexe | 6+ sprints · 3–6 mois | Eurostat + data EU | Produit exportable |

**Ordre recommandé :**
1. 🟢 **Maintenant** — C (Observatoire IRD) + D (Conférences)
2. 🟡 **Bientôt** — A (Livre) + E (Think tanks — attendre retours emails)
3. ⚪ **Plus tard** — B (API) → F (Europe)

**Notes sprint C — Observatoire IRD :**
- LinkedIn dédié bloqué : passeport périmé → page entreprise impossible pour l'instant
- Email pro `contact@portrait-elus-2026.fr` créé ✅ (redirection IONOS → Gmail)
- X (Twitter) : créer compte @IRD_France avec `contact@portrait-elus-2026.fr` dès que possible
- Bio X rédigée ✅, post de lancement rédigé ✅, template hebdo rédigé ✅ — archivés
- Créer page LinkedIn IRD dès renouvellement passeport

**À faire**
- [x] Email pro `contact@portrait-elus-2026.fr` créé ✅
- [ ] Créer compte X @IRD_France avec `contact@portrait-elus-2026.fr`
- [ ] Publier post de lancement sur @IRD_France
- [ ] Mettre en place publication hebdo (template prêt ✅)
- [ ] Créer page LinkedIn IRD dès renouvellement passeport
- [ ] Définir format publication hebdo (commune + score + commentaire)
- [ ] Commencer la structure du livre avec l'IA (sprint A)
- [ ] Réfléchir modèle API : tarification, clients cibles (sprint B)
- [ ] Mise à jour RNE dès publication par le Ministère

---

## 💬 Notes de session

- **25/03/2026** — Choix Option B. Données RNE identifiées. Structure projet définie.
- **26/03/2026** — App complète déployée. Publiée sur data.gouv.fr.
- **27/03/2026** — Page Diversité finalisée. Idée IRD identifiée.
- **29/03/2026** — Page IRD finalisée. IRD.md créé.
- **01/04/2026** — Projet terminé : footer, carte choroplèthe IRD.
- **08/04/2026** — Corrections : crash Python 3.14, badge défi, suppression INSEE 50Mo.
- **14/04/2026** — VICTOIRE : sélectionné par data.gouv.fr pour le Défi 2.
- **24/04/2026** — IRD V2 déployé (INSEE par commune). UptimeRobot configuré. Article LinkedIn publié.
- **27/04/2026** — Migration Railway + domaine custom :
  - App déployée sur Railway (europe-west4, Python 3.12, pas de mise en veille)
  - Procfile créé pour démarrage Streamlit sur Railway
  - Domaine `www.portrait-elus-2026.fr` configuré chez IONOS (CNAME + TXT)
  - DNS validés par Railway ✅, SSL en cours de génération
  - Redirection IONOS : `portrait-elus-2026.fr` → `www.portrait-elus-2026.fr`
  - Idées entrepreneuriales identifiées : livre, API, observatoire média, conférences, think tanks, version européenne
- **28/04/2026** — Finalisation domaine + mises à jour :
  - Redirection IONOS corrigée de `http://` vers `https://www.portrait-elus-2026.fr` ✅
  - SSL actif sur `www.portrait-elus-2026.fr` ✅
  - Lien mis à jour sur data.gouv.fr ✅
  - Article LinkedIn pointe déjà vers le bon domaine ✅
  - UptimeRobot reste sur Streamlit (rôle : anti-veille backup) ✅
  - Pitch deck IRD citoyen créé (`pitch_IRD_2026.pptx` + PDF) ✅
  - Pitch deck recruteur créé (`pitch_recruteur_2026.pptx` + PDF) ✅
  - Emails rédigés et archivés : journalistes (Phase 1), think tanks + conférences/IEP (Phase 2) — à envoyer
  - Template email maires rédigé et archivé — à envoyer
  - Email pro `contact@portrait-elus-2026.fr` créé ✅ (redirection IONOS → Gmail)
  - Compte X @IRD_France : création reportée — LinkedIn prioritaire pour l'instant
  - Bio X, post lancement, template hebdo rédigés et archivés — prêts quand le compte sera créé
  - **Premier engagement LinkedIn notable** : Maxime Delacarte (avocat pénaliste, Bourgeois Iztkovitch & Delacarte) a commenté le post — 177 impressions

---

## 🔗 Liens utiles

- **App principale** : https://www.portrait-elus-2026.fr ✅
- **App Railway** : https://portrait-elus-2026-production.up.railway.app
- **App Streamlit** (backup) : https://portrait-elus-2026.streamlit.app
- Réutilisation data.gouv.fr : https://www.data.gouv.fr/reuses/portrait-des-elus-municipaux-2026
- GitHub : https://github.com/raymondgadji/portrait-elus-2026
- Article LinkedIn : https://www.linkedin.com/pulse/titre-les-%25C3%25A9lus-fran%25C3%25A7ais-vous-ressemblent-ils-vraiment-raymond-gadji-olw0e
- Post victoire data.gouv.fr : https://www.linkedin.com/posts/data-gouv-fr_opendata-municipales2026-donnaezespubliques-activity-7452713070923182081-n7K7
- Défi officiel : https://defis.data.gouv.fr/defis/elections-municipales-2026-profils-des-elus
- RNE dataset : https://www.data.gouv.fr/datasets/repertoire-national-des-elus-1
- LinkedIn Raymond : https://www.linkedin.com/in/raymond-gadji/
