"""
check_rne.py — Comparaison données RNE mars vs mai 2026
Exécuter depuis la racine du projet : python check_rne.py
"""
import requests
import pandas as pd
import io
from datetime import date

print("Téléchargement RNE maires...")
r = requests.get(
    "https://www.data.gouv.fr/api/1/datasets/r/2876a346-d50c-4911-934e-19ee07b0e503",
    timeout=60
)
maires = pd.read_csv(io.BytesIO(r.content), sep=";", encoding="latin-1", low_memory=False)

print("Téléchargement RNE conseillers...")
r2 = requests.get(
    "https://www.data.gouv.fr/api/1/datasets/r/d5f400de-ae3f-4966-8cb6-a85c70c6c24a",
    timeout=120
)
cons = pd.read_csv(io.BytesIO(r2.content), sep=";", encoding="latin-1", low_memory=False)

# Colonnes par position
sexe_m   = maires.iloc[:, 8]
ddn_m    = maires.iloc[:, 9]
sexe_c   = cons.iloc[:, 8]
ddn_c    = cons.iloc[:, 9]

# Calcul âge
aujourd_hui = date.today()
def calc_age(s):
    try:
        s = str(s).strip()
        if "-" in s and s[4] == "-":
            a, m, j = s.split("-")
        else:
            j, m, a = s.split("/")
        return (aujourd_hui - date(int(a), int(m), int(j))).days // 365
    except:
        return None

age_m = ddn_m.apply(calc_age)
age_c = ddn_c.apply(calc_age)

print("\n" + "="*50)
print("COMPARAISON RNE — MARS vs MAI 2026")
print("="*50)
print(f"\n{'':25} {'MARS 2026':>12} {'MAI 2026':>12} {'ÉVOLUTION':>12}")
print("-"*65)
print(f"{'Nb maires':25} {'34 874':>12} {len(maires):>12,} {len(maires)-34874:>+12,}")
print(f"{'Nb conseillers':25} {'485 827':>12} {len(cons):>12,} {len(cons)-485827:>+12,}")
print(f"{'% femmes maires':25} {'22.8%':>12} {(sexe_m=='F').mean()*100:>11.1f}% {'':>12}")
print(f"{'% femmes conseillers':25} {'48.1%':>12} {(sexe_c=='F').mean()*100:>11.1f}% {'':>12}")
print(f"{'Âge moyen maires':25} {'59.2 ans':>12} {age_m.dropna().mean():>10.1f} ans {'':>12}")
print(f"{'Âge moyen conseillers':25} {'52.6 ans':>12} {age_c.dropna().mean():>10.1f} ans {'':>12}")
print("="*50)