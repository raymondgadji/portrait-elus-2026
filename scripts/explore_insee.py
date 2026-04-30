import pandas as pd
import zipfile, requests, io

URL = "https://www.insee.fr/fr/statistiques/fichier/5359146/dossier_complet.zip"
print("Téléchargement...")
r = requests.get(URL, timeout=300)
z = zipfile.ZipFile(io.BytesIO(r.content))
csv_name = [n for n in z.namelist() if n.endswith(".csv")][0]

with z.open(csv_name) as f:
    df = pd.read_csv(f, sep=";", encoding="utf-8",
                     low_memory=False, dtype={"CODGEO": str}, nrows=2)

cols_pop = [c for c in df.columns if "POP" in c.upper()][:20]
cols_cs  = [c for c in df.columns if "CS" in c.upper()][:20]
cols_age = [c for c in df.columns if "AGE" in c.upper() or "MED" in c.upper()][:20]

print("=== POP ===")
print(cols_pop)
print("=== CS ===")
print(cols_cs)
print("=== AGE/MED ===")
print(cols_age)