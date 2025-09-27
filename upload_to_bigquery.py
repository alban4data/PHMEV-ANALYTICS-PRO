"""
🚀 Script d'upload des données PHMEV vers Google BigQuery
Charge le fichier OPEN_PHMEV_2024.parquet vers BigQuery pour l'application Streamlit
"""

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import os
from datetime import datetime

def upload_phmev_to_bigquery():
    """Upload des données PHMEV vers BigQuery"""
    
    print("🚀 Début de l'upload PHMEV vers BigQuery...")
    
    # Configuration
    PROJECT_ID = 'test-db-473321'
    DATASET_ID = 'dataset'
    TABLE_ID = 'PHMEV2024'
    
    # Chemin du fichier parquet
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parquet_path = os.path.join(script_dir, 'OPEN_PHMEV_2024.parquet')
    
    if not os.path.exists(parquet_path):
        print(f"❌ Fichier non trouvé: {parquet_path}")
        return False
    
    try:
        # Initialiser le client BigQuery
        print("🔗 Connexion à BigQuery...")
        client = bigquery.Client(project=PROJECT_ID)
        
        # Référence de la table
        table_ref = client.dataset(DATASET_ID).table(TABLE_ID)
        
        # Charger le fichier parquet
        print(f"📊 Chargement du fichier parquet: {parquet_path}")
        df = pd.read_parquet(parquet_path, engine='pyarrow')
        
        print(f"✅ Fichier chargé: {len(df):,} lignes, {len(df.columns)} colonnes")
        
        # Nettoyer les données (identique à la version DuckDB)
        print("🔄 Nettoyage des données...")
        
        # Filtrer les entrées non informatives
        df_clean = df[
            (~df['l_cip13'].isin(['Non restitué', 'Non spécifié', 'Honoraires de dispensation'])) &
            (df['l_cip13'].notna())
        ].copy()
        
        print(f"✅ Après nettoyage: {len(df_clean):,} lignes")
        
        # Convertir les types problématiques
        print("🔧 Conversion des types de données...")
        
        # Convertir les colonnes ATC en string pour éviter les problèmes de types mixtes
        atc_columns = ['ATC5', 'atc1', 'atc2', 'atc3', 'atc4']
        for col in atc_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(str)
        
        # S'assurer que les colonnes financières sont numériques
        financial_columns = ['REM', 'BSE', 'BOITES']
        for col in financial_columns:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
        
        # Configuration du job d'upload
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",  # Remplacer la table existante
            source_format=bigquery.SourceFormat.PARQUET,
            autodetect=True,  # Détection automatique du schéma
            max_bad_records=1000  # Tolérer quelques erreurs
        )
        
        print(f"📤 Upload vers BigQuery: {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")
        print(f"📊 Nombre de lignes à uploader: {len(df_clean):,}")
        
        # Lancer le job d'upload
        job = client.load_table_from_dataframe(
            df_clean, 
            table_ref, 
            job_config=job_config
        )
        
        print("⏳ Upload en cours...")
        job.result()  # Attendre la fin du job
        
        # Vérifier le résultat
        table = client.get_table(table_ref)
        print(f"✅ Upload terminé avec succès!")
        print(f"📊 Lignes dans BigQuery: {table.num_rows:,}")
        print(f"💾 Taille de la table: {table.num_bytes / (1024*1024):.1f} MB")
        
        # Test de requête simple
        print("🧪 Test de requête...")
        test_query = f"""
        SELECT COUNT(*) as total_rows,
               COUNT(DISTINCT nom_etb) as unique_etablissements,
               COUNT(DISTINCT L_ATC5) as unique_medicaments,
               SUM(REM) as total_remboursement
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        LIMIT 1
        """
        
        result = client.query(test_query).to_dataframe()
        print("📊 Statistiques de la table:")
        print(f"   - Lignes totales: {result['total_rows'].iloc[0]:,}")
        print(f"   - Établissements uniques: {result['unique_etablissements'].iloc[0]:,}")
        print(f"   - Médicaments uniques: {result['unique_medicaments'].iloc[0]:,}")
        print(f"   - Remboursement total: {result['total_remboursement'].iloc[0]:,.2f}€")
        
        print("🎉 Upload PHMEV vers BigQuery terminé avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'upload: {e}")
        print(f"🔍 Type d'erreur: {type(e).__name__}")
        return False

def create_bigquery_views():
    """Crée des vues optimisées dans BigQuery"""
    
    print("🏗️ Création des vues optimisées...")
    
    PROJECT_ID = 'test-db-473321'
    DATASET_ID = 'dataset'
    
    try:
        client = bigquery.Client(project=PROJECT_ID)
        
        # Vue pour les établissements
        view_etablissements = f"""
        CREATE OR REPLACE VIEW `{PROJECT_ID}.{DATASET_ID}.vue_etablissements` AS
        SELECT 
            COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié') as etablissement,
            COALESCE(NULLIF(categorie_jur, ''), 'Non spécifiée') as categorie,
            COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée') as ville,
            COALESCE(region_etb, 0) as region,
            SUM(REM) as total_remboursement,
            SUM(BSE) as total_base_remboursable,
            SUM(BOITES) as total_boites,
            COUNT(*) as nb_lignes,
            AVG(CASE WHEN BOITES > 0 THEN REM / BOITES ELSE 0 END) as cout_moyen_par_boite,
            AVG(CASE WHEN BSE > 0 THEN (REM / BSE) * 100 ELSE 0 END) as taux_remboursement_moyen
        FROM `{PROJECT_ID}.{DATASET_ID}.PHMEV2024`
        WHERE l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')
        AND l_cip13 IS NOT NULL
        GROUP BY etablissement, categorie, ville, region
        """
        
        client.query(view_etablissements).result()
        print("✅ Vue établissements créée")
        
        # Vue pour les médicaments
        view_medicaments = f"""
        CREATE OR REPLACE VIEW `{PROJECT_ID}.{DATASET_ID}.vue_medicaments` AS
        SELECT 
            COALESCE(NULLIF(L_ATC5, ''), 'Non spécifié') as medicament,
            atc1, L_ATC1,
            atc2, L_ATC2,
            atc3, L_ATC3,
            atc4, L_ATC4,
            ATC5, L_ATC5,
            SUM(REM) as total_remboursement,
            SUM(BSE) as total_base_remboursable,
            SUM(BOITES) as total_boites,
            COUNT(*) as nb_lignes,
            COUNT(DISTINCT COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié')) as nb_etablissements,
            AVG(CASE WHEN BOITES > 0 THEN REM / BOITES ELSE 0 END) as cout_moyen_par_boite,
            AVG(CASE WHEN BSE > 0 THEN (REM / BSE) * 100 ELSE 0 END) as taux_remboursement_moyen
        FROM `{PROJECT_ID}.{DATASET_ID}.PHMEV2024`
        WHERE l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')
        AND l_cip13 IS NOT NULL
        GROUP BY medicament, atc1, L_ATC1, atc2, L_ATC2, atc3, L_ATC3, atc4, L_ATC4, ATC5, L_ATC5
        """
        
        client.query(view_medicaments).result()
        print("✅ Vue médicaments créée")
        
        print("🎉 Toutes les vues ont été créées avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des vues: {e}")
        return False

if __name__ == "__main__":
    print("🏥 PHMEV Analytics Pro - Upload BigQuery")
    print("=" * 50)
    
    # Étape 1: Upload des données
    success = upload_phmev_to_bigquery()
    
    if success:
        # Étape 2: Création des vues optimisées
        create_bigquery_views()
        
        print("\n🎉 Configuration BigQuery terminée!")
        print("\n📋 Prochaines étapes:")
        print("1. Configurer les credentials dans Streamlit Cloud")
        print("2. Remplacer streamlit_app.py par streamlit_app_bigquery.py")
        print("3. Déployer sur Streamlit Cloud")
        print("\n🚀 Votre application sera ultra-performante avec BigQuery!")
    else:
        print("\n❌ Échec de l'upload. Vérifiez les credentials et la configuration.")
