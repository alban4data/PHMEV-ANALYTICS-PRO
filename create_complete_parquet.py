"""
🚀 Création du parquet complet avec TOUTES les colonnes dérivées
Directement depuis le fichier backup original
"""

import pandas as pd
import numpy as np
import os

print("🚀 Création du parquet complet avec colonnes dérivées...")

# Charger le fichier backup original (sans optimisations category qui posent problème)
source_file = "OPEN_PHMEV_2024.parquet.backup"
print(f"📖 Chargement de {source_file}...")

df = pd.read_parquet(source_file)
print(f"✅ Chargé: {len(df):,} lignes, {len(df.columns)} colonnes")

# Conversion des colonnes financières (format français)
def convert_french_decimal(series):
    """Convertit les décimaux français (virgule) en float"""
    cleaned = series.astype(str).str.strip()
    cleaned = cleaned.replace(['', 'nan', 'NaN', 'NULL', 'null'], np.nan)
    
    def clean_french_number(x):
        if pd.isna(x) or x == 'nan':
            return np.nan
        x = str(x).strip()
        if ',' in x:
            parts = x.split(',')
            if len(parts) == 2:
                entiere = parts[0].replace('.', '')
                decimale = parts[1]
                return f"{entiere}.{decimale}"
        return x.replace('.', '') if '.' in x else x
    
    cleaned = cleaned.apply(clean_french_number)
    return pd.to_numeric(cleaned, errors='coerce')

print("💰 Conversion des colonnes financières...")
df['REM'] = convert_french_decimal(df['REM'])
df['BSE'] = convert_french_decimal(df['BSE'])
df['BOITES'] = pd.to_numeric(df['BOITES'], errors='coerce')

print("🔧 Création des colonnes dérivées...")

# Toutes les colonnes dérivées nécessaires
df['etablissement'] = df['nom_etb'].astype(str).fillna('Non spécifié')
if 'raison_sociale_etb' in df.columns:
    df['etablissement'] = df['etablissement'].where(
        df['etablissement'] != 'nan', 
        df['raison_sociale_etb'].astype(str).fillna('Non spécifié')
    )

df['medicament'] = df['L_ATC5'].astype(str).fillna('Non spécifié')
df['categorie'] = df['categorie_jur'].astype(str).fillna('Non spécifiée')
df['ville'] = df['nom_ville'].astype(str).fillna('Non spécifiée')
df['region'] = df['region_etb'].fillna(0)
df['code_cip'] = df['CIP13'].astype(str)
df['libelle_cip'] = df['l_cip13'].fillna('Non spécifié')

# Calculs dérivés financiers
df['cout_par_boite'] = np.where(df['BOITES'] > 0, df['REM'] / df['BOITES'], 0)
df['taux_remboursement'] = np.where(df['BSE'] > 0, df['REM'] / df['BSE'] * 100, 0)

print(f"✅ Colonnes dérivées créées. Total: {len(df.columns)} colonnes")

# Vérification des colonnes essentielles
required_columns = ['etablissement', 'medicament', 'categorie', 'ville', 'region', 'code_cip', 'libelle_cip', 'cout_par_boite', 'taux_remboursement']
missing = [col for col in required_columns if col not in df.columns]
if missing:
    print(f"❌ Colonnes manquantes: {missing}")
else:
    print("✅ Toutes les colonnes requises sont présentes")

print("🗜️ Optimisation des types pour la compression...")

# Optimisations de types SANS category (pour éviter les problèmes)
df['BOITES'] = df['BOITES'].astype('int32')
df['REM'] = df['REM'].astype('float32')  
df['BSE'] = df['BSE'].astype('float32')
df['region_etb'] = pd.to_numeric(df['region_etb'], errors='coerce').astype('int8')
df['cout_par_boite'] = df['cout_par_boite'].astype('float32')
df['taux_remboursement'] = df['taux_remboursement'].astype('float32')

print("💾 Sauvegarde du parquet complet optimisé...")

# Sauvegarder avec compression BROTLI
df.to_parquet(
    'OPEN_PHMEV_2024_sample_10k.parquet',
    compression='brotli',
    compression_level=9,
    index=False
)

# Vérification finale
df_test = pd.read_parquet('OPEN_PHMEV_2024_sample_10k.parquet')
print(f"🧪 Vérification finale:")
print(f"  - Lignes: {len(df_test):,}")
print(f"  - Colonnes: {len(df_test.columns)}")
print(f"  - Etablissement présent: {'etablissement' in df_test.columns}")
print(f"  - Taille fichier: {os.path.getsize('OPEN_PHMEV_2024_sample_10k.parquet') / (1024*1024):.1f} MB")

print("🚀 Parquet complet créé avec succès !")
