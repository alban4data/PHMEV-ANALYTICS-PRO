"""
🗜️ Compression optimale du fichier Parquet pour Streamlit Cloud
Objectif: Réduire le parquet de 62MB à moins de 25MB pour le cloud
"""

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
from datetime import datetime

def compress_parquet_maximum():
    """Compresse le parquet avec les meilleurs algorithmes disponibles"""
    
    print("🚀 Début de la compression optimale du parquet...")
    
    # Fichier source (backup)
    source_file = "OPEN_PHMEV_2024.parquet.backup"
    
    if not os.path.exists(source_file):
        print(f"❌ Fichier source non trouvé: {source_file}")
        return
    
    print(f"📊 Taille originale: {os.path.getsize(source_file) / (1024*1024):.1f} MB")
    
    # Charger le parquet
    print("📖 Chargement du parquet original...")
    df = pd.read_parquet(source_file)
    print(f"✅ Chargé: {len(df):,} lignes, {len(df.columns)} colonnes")
    
    # Optimisations des types de données
    print("🔧 Optimisation des types de données...")
    
    # Convertir les colonnes texte en catégories (compression énorme)
    categorical_columns = [
        'nom_etb', 'raison_sociale_etb', 'categorie_jur', 'nom_ville', 
        'region_etb', 'l_cip13', 'L_ATC5', 'l_atc1', 'L_ATC2', 
        'L_ATC3', 'L_ATC4', 'atc1', 'atc2', 'atc3', 'atc4', 'ATC5'
    ]
    
    for col in categorical_columns:
        if col in df.columns:
            print(f"  📂 {col} → category")
            df[col] = df[col].astype('category')
    
    # Optimiser les colonnes numériques
    numeric_optimizations = {
        'BOITES': 'int32',  # Au lieu de int64
        'REM': 'float32',   # Au lieu de float64  
        'BSE': 'float32',   # Au lieu de float64
        'CIP13': 'int64',   # Garder int64 pour les gros codes
        'region_etb': 'int8'  # Petit entier
    }
    
    for col, dtype in numeric_optimizations.items():
        if col in df.columns:
            try:
                print(f"  🔢 {col} → {dtype}")
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(dtype)
            except Exception as e:
                print(f"  ⚠️ Erreur {col}: {e}")
    
    # Tests de différents algorithmes de compression
    compression_methods = [
        ('brotli', 'BROTLI'),      # Le plus efficace
        ('gzip', 'GZIP'),          # Bon compromis
        ('lz4', 'LZ4'),            # Le plus rapide
        ('snappy', 'SNAPPY')       # Défaut Parquet
    ]
    
    results = []
    
    for method_name, method_code in compression_methods:
        try:
            print(f"\n🗜️ Test compression {method_name.upper()}...")
            
            output_file = f"OPEN_PHMEV_2024_compressed_{method_name}.parquet"
            
            # Conversion en PyArrow Table pour contrôle fin
            table = pa.Table.from_pandas(df)
            
            # Écriture avec compression maximale
            pq.write_table(
                table, 
                output_file,
                compression=method_code,
                compression_level=9 if method_name in ['brotli', 'gzip'] else None,
                use_dictionary=True,      # Compression dictionnaire
                row_group_size=50000,     # Groupes plus petits
                data_page_size=1024*1024, # Pages optimisées
                write_statistics=True,    # Stats pour optimisation
                use_deprecated_int96_timestamps=False
            )
            
            # Vérifier la taille
            size_mb = os.path.getsize(output_file) / (1024*1024)
            print(f"✅ {method_name}: {size_mb:.1f} MB")
            
            results.append((method_name, size_mb, output_file))
            
        except Exception as e:
            print(f"❌ Erreur {method_name}: {e}")
    
    # Trouver la meilleure compression
    if results:
        results.sort(key=lambda x: x[1])  # Trier par taille
        best_method, best_size, best_file = results[0]
        
        print(f"\n🏆 MEILLEURE COMPRESSION: {best_method.upper()}")
        print(f"📊 Taille finale: {best_size:.1f} MB")
        print(f"📉 Réduction: {((62 - best_size) / 62 * 100):.1f}%")
        
        # Renommer le meilleur fichier
        final_file = "OPEN_PHMEV_2024_optimized.parquet"
        if os.path.exists(final_file):
            os.remove(final_file)
        os.rename(best_file, final_file)
        
        # Nettoyer les autres fichiers
        for method, size, file in results[1:]:
            if os.path.exists(file):
                os.remove(file)
        
        print(f"✅ Fichier final: {final_file}")
        
        # Test de lecture pour vérifier
        print("\n🧪 Test de lecture du fichier optimisé...")
        df_test = pd.read_parquet(final_file)
        print(f"✅ Lecture OK: {len(df_test):,} lignes")
        
        return final_file
    
    else:
        print("❌ Aucune compression n'a fonctionné")
        return None

def create_cloud_ready_parquet():
    """Crée un parquet spécialement optimisé pour Streamlit Cloud (< 25MB)"""
    
    print("\n🌥️ Création du parquet Cloud-Ready...")
    
    source_file = "OPEN_PHMEV_2024.parquet.backup"
    df = pd.read_parquet(source_file)
    
    # Stratégie: échantillon stratifié intelligent
    print("🎯 Échantillonnage stratifié...")
    
    # Garder tous les établissements importants
    df_sorted = df.sort_values(['BOITES', 'REM'], ascending=False)
    
    # Prendre les 50k lignes les plus importantes
    df_sample = df_sorted.head(50000).copy()
    
    # Optimisations types
    categorical_cols = ['nom_etb', 'categorie_jur', 'nom_ville', 'l_cip13', 'L_ATC5']
    for col in categorical_cols:
        if col in df_sample.columns:
            df_sample[col] = df_sample[col].astype('category')
    
    # Compression BROTLI maximale
    output_file = "OPEN_PHMEV_2024_cloud.parquet"
    
    table = pa.Table.from_pandas(df_sample)
    pq.write_table(
        table, 
        output_file,
        compression='BROTLI',
        compression_level=9,
        use_dictionary=True,
        row_group_size=25000
    )
    
    size_mb = os.path.getsize(output_file) / (1024*1024)
    print(f"✅ Parquet Cloud: {size_mb:.1f} MB ({len(df_sample):,} lignes)")
    
    return output_file

if __name__ == "__main__":
    print("🗜️ COMPRESSION OPTIMALE PARQUET POUR STREAMLIT CLOUD")
    print("=" * 60)
    
    # Test 1: Compression maximale du fichier complet
    compressed_file = compress_parquet_maximum()
    
    # Test 2: Version cloud avec échantillon optimisé
    cloud_file = create_cloud_ready_parquet()
    
    print("\n🎯 RÉSULTATS FINAUX:")
    print("=" * 40)
    
    if compressed_file and os.path.exists(compressed_file):
        size = os.path.getsize(compressed_file) / (1024*1024)
        print(f"📦 Fichier compressé: {compressed_file} ({size:.1f} MB)")
    
    if cloud_file and os.path.exists(cloud_file):
        size = os.path.getsize(cloud_file) / (1024*1024)
        print(f"☁️ Fichier cloud: {cloud_file} ({size:.1f} MB)")
    
    print("\n🚀 Prêt pour Streamlit Cloud!")
