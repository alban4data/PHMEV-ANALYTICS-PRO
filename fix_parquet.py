"""
🔧 Correction rapide du parquet - Ajouter les colonnes dérivées manquantes
"""

import pandas as pd
import numpy as np

print("🔧 Correction du parquet avec colonnes dérivées...")

# Charger le parquet actuel
df = pd.read_parquet('OPEN_PHMEV_2024_sample_10k.parquet')
print(f"📊 Chargé: {len(df):,} lignes, {len(df.columns)} colonnes")

# Vérifier les colonnes existantes
print("📋 Colonnes actuelles:", df.columns.tolist()[:10])

# Créer les colonnes dérivées manquantes
print("🔧 Création des colonnes dérivées...")

# Colonnes dérivées nécessaires pour l'app
if 'etablissement' not in df.columns:
    df['etablissement'] = df['nom_etb'].astype(str).fillna('Non spécifié')
    if 'raison_sociale_etb' in df.columns:
        df['etablissement'] = df['etablissement'].where(
            df['etablissement'] != 'nan', 
            df['raison_sociale_etb'].astype(str)
        )
    print("✅ etablissement créée")

if 'medicament' not in df.columns:
    df['medicament'] = df['L_ATC5'].astype(str).fillna('Non spécifié')
    print("✅ medicament créée")

if 'categorie' not in df.columns:
    df['categorie'] = df['categorie_jur'].astype(str).fillna('Non spécifiée')
    print("✅ categorie créée")

if 'ville' not in df.columns:
    df['ville'] = df['nom_ville'].astype(str).fillna('Non spécifiée')
    print("✅ ville créée")

if 'region' not in df.columns:
    df['region'] = df['region_etb'].fillna(0)
    print("✅ region créée")

if 'code_cip' not in df.columns:
    df['code_cip'] = df['CIP13'].astype(str)
    print("✅ code_cip créée")

if 'libelle_cip' not in df.columns:
    df['libelle_cip'] = df['l_cip13'].fillna('Non spécifié')
    print("✅ libelle_cip créée")

# Calculs dérivés financiers
if 'cout_par_boite' not in df.columns:
    df['cout_par_boite'] = np.where(df['BOITES'] > 0, df['REM'] / df['BOITES'], 0)
    print("✅ cout_par_boite créée")

if 'taux_remboursement' not in df.columns:
    df['taux_remboursement'] = np.where(df['BSE'] > 0, df['REM'] / df['BSE'] * 100, 0)
    print("✅ taux_remboursement créée")

print(f"🎯 Total colonnes après correction: {len(df.columns)}")

# Sauvegarder le parquet corrigé
df.to_parquet('OPEN_PHMEV_2024_sample_10k.parquet', compression='brotli')
print("✅ Parquet corrigé sauvegardé !")

# Vérification finale
df_test = pd.read_parquet('OPEN_PHMEV_2024_sample_10k.parquet')
print(f"🧪 Test final: {len(df_test)} lignes, etablissement: {'etablissement' in df_test.columns}")
print("🚀 Correction terminée !")
