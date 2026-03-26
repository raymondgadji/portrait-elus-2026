# -*- coding: utf-8 -*-
"""
explore_data.py
---------------
Script d'exploration des donnees RNE (Repertoire National des Elus)
Version sans emojis - compatible Windows

Usage :
    python explore_data.py > exploration_resultats.txt
"""

import sys
import pandas as pd

# Force l'encodage UTF-8 pour la sortie fichier
sys.stdout.reconfigure(encoding="utf-8")

SEP = ";"
ENCODING = "utf-8"  # changer en "latin-1" si erreur

FICHIER_MAIRES      = "data/raw/elus-maires-mai.csv"
FICHIER_CONSEILLERS = "data/raw/elus-conseillers-municipaux-cm.csv"

# ─────────────────────────────────────────
# 1. CHARGEMENT
# ─────────────────────────────────────────

print("=" * 60)
print("CHARGEMENT DES FICHIERS")
print("=" * 60)

try:
    maires = pd.read_csv(FICHIER_MAIRES, sep=SEP, encoding=ENCODING, low_memory=False)
    print(f"OK maires charge        : {len(maires):,} lignes, {len(maires.columns)} colonnes")
except Exception as e:
    print(f"ERREUR maires : {e}")
    print("   --> Essaie ENCODING = 'latin-1'")
    maires = None

try:
    conseillers = pd.read_csv(FICHIER_CONSEILLERS, sep=SEP, encoding=ENCODING, low_memory=False)
    print(f"OK conseillers charge   : {len(conseillers):,} lignes, {len(conseillers.columns)} colonnes")
except Exception as e:
    print(f"ERREUR conseillers : {e}")
    conseillers = None

# ─────────────────────────────────────────
# 2. COLONNES
# ─────────────────────────────────────────

if maires is not None:
    print("\n" + "=" * 60)
    print("COLONNES DE maires")
    print("=" * 60)
    for i, col in enumerate(maires.columns):
        print(f"  {i:02d}. {col}")

    print("\n" + "=" * 60)
    print("APERCU maires (3 premieres lignes)")
    print("=" * 60)
    print(maires.head(3).to_string())

if conseillers is not None:
    print("\n" + "=" * 60)
    print("COLONNES DE conseillers")
    print("=" * 60)
    for i, col in enumerate(conseillers.columns):
        print(f"  {i:02d}. {col}")

    print("\n" + "=" * 60)
    print("APERCU conseillers (3 premieres lignes)")
    print("=" * 60)
    print(conseillers.head(3).to_string())

# ─────────────────────────────────────────
# 3. VALEURS MANQUANTES
# ─────────────────────────────────────────

for label, df in [("maires", maires), ("conseillers", conseillers)]:
    if df is not None:
        print("\n" + "=" * 60)
        print(f"VALEURS MANQUANTES --- {label}")
        print("=" * 60)
        nulls = df.isnull().sum()
        nulls_pct = (nulls / len(df) * 100).round(1)
        missing = pd.DataFrame({"manquants": nulls, "pct (%)": nulls_pct})
        result = missing[missing["manquants"] > 0]
        print("Aucune valeur manquante !" if result.empty else result.to_string())

# ─────────────────────────────────────────
# 4. STATS RAPIDES --- MAIRES
# ─────────────────────────────────────────

if maires is not None:
    print("\n" + "=" * 60)
    print("STATISTIQUES RAPIDES --- maires")
    print("=" * 60)

    col_sexe = next((c for c in maires.columns if "sexe" in c.lower()), None)
    if col_sexe:
        print(f"\nRepartition par sexe (colonne : '{col_sexe}') :")
        total = len(maires)
        for val, count in maires[col_sexe].value_counts().items():
            print(f"   {val} : {count:,} ({count/total*100:.1f}%)")
    else:
        print("\nColonne sexe : NON TROUVEE")
        print("Toutes les colonnes :", list(maires.columns))

    col_ddn = next((c for c in maires.columns if "naissance" in c.lower()), None)
    if col_ddn:
        print(f"\nDate de naissance (colonne : '{col_ddn}')")
        print(f"   Exemples : {maires[col_ddn].dropna().head(5).tolist()}")

    col_dep = next((c for c in maires.columns if "partement" in c.lower()), None)
    if col_dep:
        print(f"\nDepartements (colonne : '{col_dep}')")
        print(f"   Nb uniques : {maires[col_dep].nunique()}")
        print(f"   Exemples   : {sorted(maires[col_dep].dropna().astype(str).unique())[:10]}")

    col_csp = next((c for c in maires.columns if "profession" in c.lower() or "csp" in c.lower() or "cat" in c.lower()), None)
    if col_csp:
        print(f"\nTop 10 professions (colonne : '{col_csp}') :")
        print(maires[col_csp].value_counts().head(10).to_string())

    col_fonc = next((c for c in maires.columns if "fonction" in c.lower()), None)
    if col_fonc:
        print(f"\nFonctions (colonne : '{col_fonc}') :")
        print(maires[col_fonc].value_counts().to_string())

print("\n" + "=" * 60)
print("Exploration terminee !")
print("Ouvre exploration_resultats.txt dans VS Code et envoie a Claude.")
print("=" * 60)