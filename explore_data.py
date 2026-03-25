"""
explore_data.py
---------------
Script d'exploration des données RNE (Répertoire National des Élus)
À lancer UNE SEULE FOIS pour comprendre la structure des données.

Usage :
    python explore_data.py
"""

import pandas as pd

SEP = ";"  # séparateur CSV du RNE
ENCODING = "utf-8"  # essayer "latin-1" si erreur d'encodage

# ─────────────────────────────────────────────
# 1. CHARGEMENT
# ─────────────────────────────────────────────

print("=" * 60)
print("📂 CHARGEMENT DES FICHIERS")
print("=" * 60)

try:
    maires = pd.read_csv(
        "data/raw/maires.csv",
        sep=SEP,
        encoding=ENCODING,
        low_memory=False
    )
    print(f"✅ maires.csv chargé : {len(maires):,} lignes")
except Exception as e:
    print(f"❌ Erreur maires.csv : {e}")
    print("   → Essaie de changer ENCODING = 'latin-1' en haut du script")
    maires = None

try:
    conseillers = pd.read_csv(
        "data/raw/conseillers.csv",
        sep=SEP,
        encoding=ENCODING,
        low_memory=False
    )
    print(f"✅ conseillers.csv chargé : {len(conseillers):,} lignes")
except Exception as e:
    print(f"❌ Erreur conseillers.csv : {e}")
    conseillers = None


# ─────────────────────────────────────────────
# 2. COLONNES DISPONIBLES
# ─────────────────────────────────────────────

if maires is not None:
    print("\n" + "=" * 60)
    print("📋 COLONNES DE maires.csv")
    print("=" * 60)
    for i, col in enumerate(maires.columns):
        print(f"  {i:02d}. {col}")

    print("\n" + "=" * 60)
    print("🔍 APERÇU maires.csv (5 premières lignes)")
    print("=" * 60)
    print(maires.head(5).to_string())

if conseillers is not None:
    print("\n" + "=" * 60)
    print("📋 COLONNES DE conseillers.csv")
    print("=" * 60)
    for i, col in enumerate(conseillers.columns):
        print(f"  {i:02d}. {col}")


# ─────────────────────────────────────────────
# 3. VALEURS MANQUANTES
# ─────────────────────────────────────────────

if maires is not None:
    print("\n" + "=" * 60)
    print("🕳️  VALEURS MANQUANTES — maires.csv")
    print("=" * 60)
    nulls = maires.isnull().sum()
    nulls_pct = (nulls / len(maires) * 100).round(1)
    missing = pd.DataFrame({"manquants": nulls, "pct": nulls_pct})
    print(missing[missing["manquants"] > 0].to_string())


# ─────────────────────────────────────────────
# 4. STATISTIQUES RAPIDES
# ─────────────────────────────────────────────

if maires is not None:
    print("\n" + "=" * 60)
    print("📊 STATISTIQUES RAPIDES — maires.csv")
    print("=" * 60)

    # Chercher la colonne sexe (le nom peut varier)
    col_sexe = None
    for col in maires.columns:
        if "sexe" in col.lower() or "sex" in col.lower():
            col_sexe = col
            break

    if col_sexe:
        print(f"\n👤 Répartition par sexe (colonne : '{col_sexe}') :")
        print(maires[col_sexe].value_counts())
        total = len(maires)
        for val, count in maires[col_sexe].value_counts().items():
            print(f"   → {val} : {count:,} ({count/total*100:.1f}%)")

    # Chercher la colonne date de naissance
    col_ddn = None
    for col in maires.columns:
        if "naissance" in col.lower() or "birth" in col.lower():
            col_ddn = col
            break

    if col_ddn:
        print(f"\n🎂 Colonne date de naissance détectée : '{col_ddn}'")
        print(f"   Exemple de valeurs : {maires[col_ddn].dropna().head(5).tolist()}")

    # Chercher la colonne département
    col_dep = None
    for col in maires.columns:
        if "département" in col.lower() or "departement" in col.lower():
            col_dep = col
            break

    if col_dep:
        print(f"\n🗺️  Nb de départements uniques : {maires[col_dep].nunique()}")
        print(f"   Exemples : {maires[col_dep].unique()[:10].tolist()}")

    # Chercher la colonne CSP/profession
    col_csp = None
    for col in maires.columns:
        if "profession" in col.lower() or "csp" in col.lower() or "catégorie" in col.lower():
            col_csp = col
            break

    if col_csp:
        print(f"\n💼 Top 10 professions (colonne : '{col_csp}') :")
        print(maires[col_csp].value_counts().head(10).to_string())


print("\n" + "=" * 60)
print("✅ Exploration terminée !")
print("   Copie-colle la sortie de ce script et envoie-la à Claude.")
print("=" * 60)