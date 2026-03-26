"""
utils/loader.py
---------------
Chargement des données RNE avec téléchargement automatique.
Sur Streamlit Cloud : télécharge depuis data.gouv.fr au premier lancement.
En local : utilise les fichiers déjà présents dans data/raw/.
"""

import os
import requests
import pandas as pd
import streamlit as st
from datetime import date
from pathlib import Path

# ── URLs officielles data.gouv.fr ──────────────────────────────────────────
URL_MAIRES      = "https://www.data.gouv.fr/api/1/datasets/r/2876a346-d50c-4911-934e-19ee07b0e503"
URL_CONSEILLERS = "https://www.data.gouv.fr/api/1/datasets/r/d5f400de-ae3f-4966-8cb6-a85c70c6c24a"

FICHIER_MAIRES      = Path("data/raw/elus-maires-mai.csv")
FICHIER_CONSEILLERS = Path("data/raw/elus-conseillers-municipaux-cm.csv")

SEP      = ";"
ENCODING = "latin-1"


# ── Téléchargement ──────────────────────────────────────────────────────────

def _telecharger(url: str, destination: Path) -> None:
    """Télécharge un fichier CSV depuis data.gouv.fr si absent."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with st.spinner(f"Téléchargement des données depuis data.gouv.fr…"):
        r = requests.get(url, timeout=120)
        r.raise_for_status()
        destination.write_bytes(r.content)


def _assurer_presence(fichier: Path, url: str) -> None:
    """Vérifie que le fichier existe, sinon le télécharge."""
    if not fichier.exists():
        _telecharger(url, fichier)


# ── Nettoyage ───────────────────────────────────────────────────────────────

def _calculer_age(serie_ddn: pd.Series) -> pd.Series:
    """Calcule l'âge en Python pur — compatible Python 3.13."""
    aujourd_hui = date.today()
    def age_depuis_str(s):
        try:
            j, m, a = str(s).split("/")
            naissance = date(int(a), int(m), int(j))
            return (aujourd_hui - naissance).days // 365
        except Exception:
            return None
    return serie_ddn.apply(age_depuis_str)


def _renommer_par_position(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """Renomme les colonnes par index pour éviter les problèmes d'encodage."""
    cols = list(df.columns)
    for idx, nom in mapping.items():
        if idx < len(cols):
            cols[idx] = nom
    df.columns = cols
    return df


def _corriger_encodage(serie: pd.Series) -> pd.Series:
    """Corrige le double-encodage latin-1/utf-8 sur les noms de lieux."""
    def fix(val):
        if pd.isna(val):
            return val
        try:
            return str(val).encode("latin-1").decode("utf-8")
        except Exception:
            return str(val)
    return serie.apply(fix)


def _ajouter_tranches_age(df: pd.DataFrame) -> pd.DataFrame:
    bins   = [0, 29, 39, 49, 59, 69, 79, 120]
    labels = ["< 30", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]
    df["tranche_age"] = pd.cut(df["age"], bins=bins, labels=labels, right=True)
    return df


# ── Chargement principal ────────────────────────────────────────────────────

@st.cache_data(show_spinner="Chargement des données maires…")
def charger_maires() -> pd.DataFrame:
    _assurer_presence(FICHIER_MAIRES, URL_MAIRES)

    df = pd.read_csv(FICHIER_MAIRES, sep=SEP, encoding=ENCODING,
                     low_memory=False, header=0)

    df = _renommer_par_position(df, {
        0 : "code_dep",
        1 : "dep",
        2 : "code_csp_particulier",
        3 : "csp_particulier",
        4 : "code_commune",
        5 : "commune",
        6 : "nom",
        7 : "prenom",
        8 : "sexe",
        9 : "date_naissance",
        10: "code_csp",
        11: "csp",
        12: "date_mandat",
        13: "date_fonction",
    })

    for col in ["dep", "commune", "nom", "prenom", "csp"]:
        df[col] = _corriger_encodage(df[col])

    df["age"] = _calculer_age(df["date_naissance"])
    df = _ajouter_tranches_age(df)
    df["code_dep"] = df["code_dep"].astype(str).str.strip().str.zfill(2)

    return df


@st.cache_data(show_spinner="Chargement des données conseillers…")
def charger_conseillers() -> pd.DataFrame:
    _assurer_presence(FICHIER_CONSEILLERS, URL_CONSEILLERS)

    df = pd.read_csv(FICHIER_CONSEILLERS, sep=SEP, encoding=ENCODING,
                     low_memory=False, header=0)

    df = _renommer_par_position(df, {
        0 : "code_dep",
        1 : "dep",
        2 : "code_csp_particulier",
        3 : "csp_particulier",
        4 : "code_commune",
        5 : "commune",
        6 : "nom",
        7 : "prenom",
        8 : "sexe",
        9 : "date_naissance",
        10: "code_csp",
        11: "csp",
        12: "date_mandat",
        13: "fonction",
        14: "date_fonction",
        15: "nationalite",
    })

    for col in ["dep", "commune", "nom", "prenom", "csp"]:
        df[col] = _corriger_encodage(df[col])

    df["age"] = _calculer_age(df["date_naissance"])
    df = _ajouter_tranches_age(df)
    df["code_dep"] = df["code_dep"].astype(str).str.strip().str.zfill(2)

    return df