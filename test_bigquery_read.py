"""
🔍 Test de lecture BigQuery - Vérifier les données existantes
"""

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os

def test_bigquery_read():
    """Test de lecture des données BigQuery existantes"""
    
    print("🔍 Test de lecture BigQuery...")
    
    PROJECT_ID = 'test-db-473321'
    
    try:
        # Initialiser le client BigQuery avec les credentials
        credentials_path = "test-db-473321-aed58eeb55a8.json"
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
        
        print(f"✅ Connexion réussie au projet: {PROJECT_ID}")
        
        # Lister les datasets
        print("\n📊 Datasets disponibles:")
        datasets = list(client.list_datasets())
        
        if not datasets:
            print("❌ Aucun dataset trouvé")
            return
        
        for dataset in datasets:
            print(f"  - {dataset.dataset_id}")
            
            # Lister les tables dans chaque dataset
            dataset_ref = client.dataset(dataset.dataset_id)
            tables = list(client.list_tables(dataset_ref))
            
            if tables:
                print(f"    Tables dans {dataset.dataset_id}:")
                for table in tables:
                    table_ref = client.get_table(table.reference)
                    print(f"      - {table.table_id} ({table_ref.num_rows:,} lignes, {table_ref.num_bytes / (1024*1024):.1f} MB)")
                    
                    # Si c'est une table PHMEV, tester une requête
                    if 'PHMEV' in table.table_id.upper():
                        print(f"\n🧪 Test de requête sur {table.table_id}:")
                        
                        # Requête simple pour voir la structure
                        query = f"""
                        SELECT *
                        FROM `{PROJECT_ID}.{dataset.dataset_id}.{table.table_id}`
                        LIMIT 5
                        """
                        
                        try:
                            result = client.query(query).to_dataframe()
                            print(f"✅ Requête réussie! Colonnes disponibles:")
                            for col in result.columns:
                                print(f"        - {col}")
                            
                            print(f"\n📊 Aperçu des données:")
                            print(result.head())
                            
                        except Exception as e:
                            print(f"❌ Erreur de requête: {e}")
            else:
                print(f"    Aucune table dans {dataset.dataset_id}")
        
        # Test de requête sur des tables publiques si aucune donnée PHMEV
        print("\n🌐 Test d'accès aux données publiques BigQuery...")
        
        public_query = """
        SELECT 
            name, 
            gender, 
            count
        FROM `bigquery-public-data.usa_names.usa_1910_current` 
        WHERE state = 'TX'
        AND gender = 'F'
        AND year = 2020
        ORDER BY count DESC
        LIMIT 5
        """
        
        try:
            public_result = client.query(public_query).to_dataframe()
            print("✅ Accès aux données publiques OK!")
            print(public_result)
        except Exception as e:
            print(f"❌ Pas d'accès aux données publiques: {e}")
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print(f"🔍 Type d'erreur: {type(e).__name__}")

if __name__ == "__main__":
    test_bigquery_read()
