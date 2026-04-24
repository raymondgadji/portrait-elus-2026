"""
scripts/prepare_insee.py
------------------------
Script à exécuter UNE SEULE FOIS en local.
Produit : data/processed/insee_light.csv (~400Ko)
"""

import pandas as pd
import zipfile, requests, io
from pathlib import Path

URL_INSEE = (
    "https://www.insee.fr/fr/statistiques/fichier/5359146/"
    "dossier_complet.zip"
)

OUTPUT = Path("data/processed/insee_light.csv")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

print("Téléchargement du fichier INSEE...")
r = requests.get(URL_INSEE, timeout=300)
r.raise_for_status()

print("Extraction...")
z = zipfile.ZipFile(io.BytesIO(r.content))
csv_name = [n for n in z.namelist() if n.endswith(".csv")][0]

with z.open(csv_name) as f:
    df = pd.read_csv(f, sep=";", encoding="utf-8",
                     low_memory=False, dtype={"CODGEO": str})

print(f"Fichier chargé : {len(df)} communes")

VARS = ["CODGEO", "P22_POP", "P22_POPF",
        "C16_POP15P_CS1", "C16_POP15P_CS2", "C16_POP15P_CS3",
        "C16_POP15P_CS4", "C16_POP15P_CS5", "C16_POP15P_CS6"]

cols = [c for c in VARS if c in df.columns]
df = df[cols].copy()

cs_cols = ["C16_POP15P_CS1", "C16_POP15P_CS2", "C16_POP15P_CS3",
           "C16_POP15P_CS4", "C16_POP15P_CS5", "C16_POP15P_CS6"]

# Conversion numérique explicite de toutes les colonnes
for col in ["P22_POP", "P22_POPF"] + cs_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# % femmes dans la population
df["pct_femmes_pop"] = (df["P22_POPF"] / df["P22_POP"] * 100).round(2)

# % cadres (CS3) parmi la population active 15+
pop_active = df[cs_cols].sum(axis=1).astype(float)
cs3 = df["C16_POP15P_CS3"].astype(float)
df["pct_cadres_pop"] = (cs3 / pop_active.where(pop_active > 0) * 100).round(2)

# Âge médian — constante nationale
df["age_median_pop"] = 42.0

# Garder uniquement les 3 colonnes utiles
df_final = df[["CODGEO", "pct_femmes_pop", "pct_cadres_pop", "age_median_pop"]].dropna()

df_final.to_csv(OUTPUT, index=False)
taille_ko = OUTPUT.stat().st_size / 1024
print(f"Fichier créé : {len(df_final)} communes — {taille_ko:.0f} Ko")
print(f"Sauvegardé : {OUTPUT}")
print("Terminé !")