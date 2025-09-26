import pandas as pd
import numpy as np
import os
from datetime import datetime

def create_sample_parquet():
    """Créer un échantillon de 10k lignes du fichier Parquet complet"""
    
    print("🚀 CRÉATION ÉCHANTILLON PARQUET 10K")
    print("=" * 50)
    print(f"⏰ Début: {datetime.now().strftime('%H:%M:%S')}")
    
    # Restaurer temporairement le fichier original
    parquet_original = 'OPEN_PHMEV_2024.parquet.backup'
    parquet_sample = 'OPEN_PHMEV_2024_sample_10k.parquet'
    
    if not os.path.exists(parquet_original):
        print("❌ Fichier original non trouvé. Vérifiez le nom du fichier backup.")
        return
    
    print("📁 Chargement du fichier complet...")
    df = pd.read_parquet(parquet_original)
    print(f"📊 Lignes totales: {len(df):,}")
    
    # Créer un échantillon stratifié pour avoir une bonne représentativité
    print("🎯 Création d'un échantillon représentatif de 10,000 lignes...")
    
    # Échantillonnage stratifié par région si possible
    if 'region_etb' in df.columns:
        # Échantillon stratifié par région
        sample_size = 10000
        region_counts = df['region_etb'].value_counts()
        
        sampled_dfs = []
        for region, count in region_counts.items():
            # Proportionnel au nombre total
            region_sample_size = int((count / len(df)) * sample_size)
            if region_sample_size < 1:
                region_sample_size = 1
            
            region_df = df[df['region_etb'] == region]
            if len(region_df) > region_sample_size:
                region_sample = region_df.sample(n=region_sample_size, random_state=42)
            else:
                region_sample = region_df
            
            sampled_dfs.append(region_sample)
        
        df_sample = pd.concat(sampled_dfs, ignore_index=True)
        
        # Ajuster si nécessaire pour avoir exactement 10k
        if len(df_sample) > sample_size:
            df_sample = df_sample.sample(n=sample_size, random_state=42)
        elif len(df_sample) < sample_size:
            # Compléter avec échantillon aléatoire
            remaining = sample_size - len(df_sample)
            additional = df.drop(df_sample.index).sample(n=remaining, random_state=42)
            df_sample = pd.concat([df_sample, additional], ignore_index=True)
    
    else:
        # Échantillon aléatoire simple
        df_sample = df.sample(n=10000, random_state=42)
    
    print(f"✅ Échantillon créé: {len(df_sample):,} lignes")
    
    # Vérifier les colonnes et les enrichir si nécessaire
    print("🔧 Vérification et enrichissement des colonnes...")
    
    if 'etablissement' not in df_sample.columns:
        df_sample['etablissement'] = df_sample['nom_etb'].astype(str).fillna('Non spécifié')
        if 'raison_sociale_etb' in df_sample.columns:
            df_sample['etablissement'] = df_sample['etablissement'].where(
                df_sample['etablissement'] != 'nan', 
                df_sample['raison_sociale_etb'].astype(str)
            )
    
    if 'medicament' not in df_sample.columns:
        df_sample['medicament'] = df_sample['L_ATC5'].astype(str).fillna('Non spécifié')
    if 'categorie' not in df_sample.columns:
        df_sample['categorie'] = df_sample['categorie_jur'].astype(str).fillna('Non spécifiée')
    if 'ville' not in df_sample.columns:
        df_sample['ville'] = df_sample['nom_ville'].astype(str).fillna('Non spécifiée')
    if 'region' not in df_sample.columns:
        df_sample['region'] = df_sample['region_etb'].fillna(0)
    if 'code_cip' not in df_sample.columns:
        df_sample['code_cip'] = df_sample['CIP13'].astype(str)
    if 'libelle_cip' not in df_sample.columns:
        df_sample['libelle_cip'] = df_sample['l_cip13'].fillna('Non spécifié')
    
    # Calculs dérivés
    if 'cout_par_boite' not in df_sample.columns:
        df_sample['cout_par_boite'] = np.where(df_sample['BOITES'] > 0, df_sample['REM'] / df_sample['BOITES'], 0)
    if 'taux_remboursement' not in df_sample.columns:
        df_sample['taux_remboursement'] = np.where(df_sample['REM'] > 0, (df_sample['BSE'] / df_sample['REM']) * 100, 0)
    
    print("💾 Sauvegarde de l'échantillon...")
    df_sample.to_parquet(parquet_sample, index=False, engine='pyarrow', compression='snappy')
    
    # Statistiques
    original_size = os.path.getsize(parquet_original) / (1024**2)
    sample_size_mb = os.path.getsize(parquet_sample) / (1024**2)
    reduction = (1 - sample_size_mb / original_size) * 100
    
    print("\n✅ ÉCHANTILLON CRÉÉ AVEC SUCCÈS!")
    print("=" * 50)
    print(f"📏 Fichier original:  {original_size:.1f} MB ({len(df):,} lignes)")
    print(f"📦 Échantillon:       {sample_size_mb:.1f} MB ({len(df_sample):,} lignes)")
    print(f"🎯 Réduction taille:  {reduction:.1f}%")
    print(f"📊 Réduction lignes:  {(1 - len(df_sample)/len(df)) * 100:.1f}%")
    print(f"⏰ Fin: {datetime.now().strftime('%H:%M:%S')}")
    
    print(f"\n🚀 Fichier créé: {parquet_sample}")
    print("🔄 Vous pouvez maintenant:")
    print("1. Ajouter ce fichier à Git")
    print("2. Le pousser vers GitHub") 
    print("3. Modifier l'app pour utiliser ce fichier")

if __name__ == "__main__":
    create_sample_parquet()
