"""
patch_badge.py
--------------
Script à exécuter UNE SEULE FOIS à la racine du projet.
Remplace le badge dans tous les fichiers pages/*.py et app.py

Usage :
    python patch_badge.py
"""

import os
import re

OLD = "DÉFI OPEN DATA · DATA.GOUV.FR · ÉLECTIONS MUNICIPALES 2026"
NEW = "🏆 LAURÉAT · DÉFI OPEN DATA · DATA.GOUV.FR · ÉLECTIONS MUNICIPALES 2026"

files_to_patch = [
    "app.py",
    "pages/1_IRD.py",
    "pages/2_parite.py",
    "pages/3_age.py",
    "pages/4_diversite.py",
    "pages/5_carte.py",
    "pages/6_professions.py",
]

total_replacements = 0

for filepath in files_to_patch:
    if not os.path.exists(filepath):
        print(f"⚠️  Fichier introuvable : {filepath}")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    count = content.count(OLD)
    if count == 0:
        print(f"✅ Déjà à jour : {filepath}")
        continue

    new_content = content.replace(OLD, NEW)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    total_replacements += count
    print(f"✅ {filepath} — {count} remplacement(s) effectué(s)")

print(f"\n🎉 Terminé — {total_replacements} remplacements au total")
print("Tu peux maintenant faire : git add . && git commit -m 'badge: lauréat' && git push")