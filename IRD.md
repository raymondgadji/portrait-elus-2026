# 🏛️ IRD — Indice de Représentativité Démocratique
> Documentation grand public — Pour comprendre l'IRD simplement

---

## 🧒 C'est quoi l'IRD, expliqué à un enfant de 7 ans ?

Imagine que tu as une classe de 30 élèves. Dans ta classe il y a des filles et des garçons, des grands et des petits, des enfants qui aiment le foot et d'autres qui préfèrent la danse.

Maintenant imagine qu'on choisit 5 enfants pour représenter toute la classe — pour décider des règles, du menu à la cantine, des sorties scolaires.

**Si ces 5 enfants sont tous des grands garçons qui aiment le foot**, est-ce qu'ils vont bien représenter tout le monde ? Probablement pas. Les filles, les petits, ceux qui aiment la danse — personne ne les représente vraiment.

**L'IRD, c'est exactement ça, mais pour les villes françaises.** C'est un score qui dit : *"Est-ce que les élus de ta ville te ressemblent ?"*

- **Score 100** → Les élus sont le miroir parfait des habitants. Parfait.
- **Score 0** → Les élus ne ressemblent pas du tout aux habitants. Problème.
- **Score moyen en France (V2) : 49.1/100** → Représentativité moyenne.

---

## 🤔 Pourquoi a-t-on créé l'IRD ?

### Le problème qu'on a voulu résoudre

En France, on parle souvent de **"crise de la démocratie"** ou de **"fossé entre les élus et les citoyens"**. Mais personne n'avait jamais mesuré ce fossé de manière concrète, commune par commune, avec un chiffre simple.

Le gouvernement a lancé un **challenge open data** en 2026 avec une question précise : *"Qui sont les élus municipaux et ressemblent-ils à la population ?"*

L'IRD est né de cette question. Au lieu de dire vaguement "les élus sont trop vieux" ou "il n'y a pas assez de femmes", on a voulu mettre un chiffre dessus — mesurable, comparable, cartographiable.

### Ce qui n'existait pas avant

Avant l'IRD, il n'existait **aucun observatoire officiel français** proposant un score synthétique de représentativité par commune. Des études existaient sur la parité, d'autres sur l'âge des élus — mais jamais les trois ensemble, jamais par commune, jamais avec un score unique de 0 à 100.

C'est la nouveauté de l'IRD : **croiser trois dimensions en un seul chiffre, pour chacune des 32 354 communes analysées**.

---

## 📐 Comment ça se calcule ?

L'IRD mesure l'écart entre **le profil des élus** et **le profil de la population** sur trois critères :

### 1. Le Genre (40% du score)
On compare le pourcentage de femmes parmi les élus avec le pourcentage de femmes dans la population de chaque commune (données INSEE 2022).

> **Exemple :** Si une ville a 30% de femmes élues, mais que sa population est composée à 51% de femmes → l'écart est de 21 points. Plus l'écart est grand, plus le score genre est bas.

### 2. L'Âge (35% du score)
On compare l'âge moyen des élus avec l'âge médian de la population nationale (42 ans).

> **Exemple :** Si les élus ont en moyenne 62 ans → l'écart est de 20 ans. Les élus sont structurellement plus vieux que la population. C'est la composante la plus déficitaire en France (score moyen V2 : 41.4/100).

### 3. La Catégorie Socio-Professionnelle — CSP (25% du score)
On compare le pourcentage de cadres et professions intellectuelles parmi les élus avec leur part dans la population active de chaque commune (données INSEE 2022).

> **Exemple :** Si 80% des élus sont cadres, avocats ou médecins, mais que les cadres ne représentent que 15% de la population active locale → les "cols blancs" sont massivement surreprésentés.

### Le calcul final
Chaque écart est transformé en score de 0 à 100 (100 = pas d'écart, 0 = écart maximal), puis on fait la **moyenne pondérée** des trois scores.

```
IRD = (score_genre × 40%) + (score_âge × 35%) + (score_CSP × 25%)
```

---

## 📊 Ce que les chiffres nous disent sur la France — Version 2 (avril 2026)

| Indicateur | Valeur V2 |
|-----------|-----------|
| Communes analysées | 32 354 |
| IRD moyen national | 49.1 / 100 |
| IRD médian | 49.2 / 100 |
| Communes avec IRD < 40 (faible) | 26.8% |
| Communes avec IRD ≥ 70 (bon) | 7.7% |
| Score genre moyen | 49.1 / 100 |
| Score âge moyen | 41.4 / 100 ← le plus déficitaire |
| Score CSP moyen | 59.9 / 100 |

**En clair :** La France est à 49.1/100 — une représentativité moyenne. C'est légèrement mieux qu'estimé en V1 (45/100) grâce aux données réelles par commune. Mais c'est loin d'être satisfaisant : plus d'un quart des communes ont une représentativité faible. Et c'est l'âge — pas le genre, pas la CSP — qui creuse le plus grand fossé entre élus et citoyens.

### Évolution V1 → V2
| Indicateur | V1 (moyennes nationales) | V2 (données par commune) |
|-----------|--------------------------|--------------------------|
| IRD moyen | 45.0/100 | **49.1/100** |
| IRD médian | 44.5/100 | **49.2/100** |
| Communes IRD < 40 | 37.6% | **26.8%** |
| Communes IRD ≥ 70 | 4.0% | **7.7%** |

La V2 utilise les vraies données de population par commune (% femmes, % cadres) au lieu des moyennes nationales uniformes — ce qui donne des scores plus précis et plus nuancés.

---

## 🏘️ À quoi ça sert concrètement ?

### Pour un maire
> *"Mon score IRD est 38/100. Je vois que mon point faible est l'âge (score 15/100). Il n'y a presque pas d'élus de moins de 40 ans dans mon conseil. Je vais cibler mes prochaines actions de mobilisation citoyenne vers les jeunes."*

L'IRD donne un **diagnostic actionnable**. Ce n'est pas une critique, c'est un outil de pilotage.

### Pour un préfet ou un ministre
> *"Les communes du Pas-de-Calais ont un IRD moyen parmi les plus bas de France. Qu'est-ce qui se passe là-bas ? Quels leviers activer ?"*

L'IRD permet de **cibler les politiques publiques** là où le déficit démocratique est le plus fort.

### Pour un chercheur ou un journaliste
> *"Les grandes villes ont-elles un meilleur IRD que les petites communes rurales ? La parité légale a-t-elle vraiment changé les choses ?"*

L'IRD ouvre des **questions de recherche** sur les déterminants de la représentativité.

### Pour un citoyen
> *"Mon élu me ressemble-t-il ? Qui parle en mon nom à la mairie ?"*

L'IRD rend la démocratie **concrète et mesurable** pour n'importe qui.

---

## 🗞️ Comment l'expliquer à un journaliste en 30 secondes ?

> *"Imaginez un thermomètre de la démocratie locale. On a calculé, pour chacune des 32 000 communes de France, à quel point les élus ressemblent aux habitants — en termes de genre, d'âge et de catégorie sociale. Le résultat : la France est à 49/100. Plus d'un quart des communes ont une représentativité faible. Et le plus grand fossé, ce n'est pas entre hommes et femmes — c'est entre les générations. Les élus ont en moyenne 20 ans de plus que leurs administrés."*

---

## 🔬 Limites et honnêteté intellectuelle

L'IRD est un **indicateur, pas une vérité absolue**. Quelques limites à connaître :

- **L'âge médian de la population** est une constante nationale (42 ans) faute de données fiables par commune dans le recensement — les scores d'âge sont donc moins précis que les scores genre et CSP.
- **La CSP des maires** est celle déclarée au RNE — des erreurs ou approximations existent dans les données sources.
- **Un score faible n'est pas une faute**. Il indique un écart, pas une intention. Une commune rurale avec un maire agriculteur de 68 ans peut très bien représenter sa population si celle-ci est majoritairement âgée et agricole.
- **L'IRD ne mesure pas la qualité de la gouvernance** — un élu très représentatif peut très mal gérer sa commune, et inversement.

---

## 📡 Sources de données

| Données | Source |
|---------|--------|
| Profil des élus (genre, âge, CSP) | Répertoire National des Élus (RNE) — Ministère de l'Intérieur |
| % femmes et % cadres par commune | Recensement de la population 2022 — INSEE |
| Âge médian population | 42 ans (constante nationale) |

Toutes les données sont **ouvertes, publiques et gratuites**. L'IRD est reproductible par n'importe qui.

---

## 🚀 Et ensuite ?

L'IRD version 2 intègre les données INSEE réelles par commune pour le genre et la CSP. Les pistes d'amélioration futures :

- Intégrer l'âge médian **par commune** (données disponibles mais volumineuses)
- Étendre le calcul aux **conseillers municipaux** (pas seulement les maires)
- Suivre l'**évolution de l'IRD dans le temps** (comparaison 2020 vs 2026)
- Transformer l'IRD en **observatoire permanent** mis à jour à chaque élection

---

*IRD créé par Raymond Gadji — Data Analyst — Lauréat du Challenge Open Data data.gouv.fr, Défi 2 : Profil des élus municipaux 2026.*
*LinkedIn : https://www.linkedin.com/in/raymond-gadji/*
*App : https://portrait-elus-2026.streamlit.app*
