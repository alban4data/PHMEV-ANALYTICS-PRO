"""
🔍 Test des différents noms de tables PHMEV possibles
"""

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

def test_phmev_tables():
    """Test différents noms de tables PHMEV"""
    
    print("🔍 Test des tables PHMEV possibles...")
    
    PROJECT_ID = 'test-db-473321'
    
    # Noms possibles pour la table et le dataset
    possible_datasets = ['dataset', 'phmev', 'pharma', 'data', 'analytics']
    possible_tables = ['PHMEV_2024', 'PHMEV2024', 'phmev_2024', 'phmev2024', 'PHMEV', 'phmev']
    
    try:
        # Initialiser le client BigQuery
        credentials_path = "test-db-473321-aed58eeb55a8.json"
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
        
        print(f"✅ Connexion réussie au projet: {PROJECT_ID}")
        
        # Tester toutes les combinaisons
        for dataset_name in possible_datasets:
            for table_name in possible_tables:
                table_path = f"`{PROJECT_ID}.{dataset_name}.{table_name}`"
                
                try:
                    query = f"SELECT COUNT(*) as count FROM {table_path} LIMIT 1"
                    result = client.query(query).result()
                    
                    # Si on arrive ici, la table existe !
                    count = list(result)[0].count
                    print(f"🎉 TROUVÉ! Table: {table_path}")
                    print(f"   📊 Nombre de lignes: {count:,}")
                    
                    # Tester la structure
                    structure_query = f"SELECT * FROM {table_path} LIMIT 3"
                    sample_data = client.query(structure_query).to_dataframe()
                    
                    print(f"   📋 Colonnes ({len(sample_data.columns)}):")
                    for i, col in enumerate(sample_data.columns):
                        if i < 10:  # Afficher seulement les 10 premières
                            print(f"      - {col}")
                        elif i == 10:
                            print(f"      - ... et {len(sample_data.columns) - 10} autres colonnes")
                            break
                    
                    print(f"\n   🔍 Aperçu des données:")
                    print(sample_data.head(2))
                    
                    return dataset_name, table_name  # Retourner la combinaison qui marche
                    
                except Exception as e:
                    # Table n'existe pas, continuer
                    if "Not found" not in str(e):
                        print(f"❌ Erreur pour {table_path}: {e}")
        
        print("❌ Aucune table PHMEV trouvée avec les noms testés")
        
        # Essayer de lister tous les datasets et tables disponibles
        print("\n🔍 Exploration complète du projet...")
        
        try:
            datasets = list(client.list_datasets())
            if datasets:
                print("📊 Tous les datasets disponibles:")
                for dataset in datasets:
                    print(f"  📁 Dataset: {dataset.dataset_id}")
                    
                    try:
                        dataset_ref = client.dataset(dataset.dataset_id)
                        tables = list(client.list_tables(dataset_ref))
                        
                        if tables:
                            for table in tables:
                                table_ref = client.get_table(table.reference)
                                print(f"    📋 Table: {table.table_id} ({table_ref.num_rows:,} lignes)")
                        else:
                            print("    (aucune table)")
                    except Exception as e:
                        print(f"    ❌ Erreur d'accès: {e}")
            else:
                print("❌ Aucun dataset trouvé dans le projet")
        except Exception as e:
            print(f"❌ Erreur lors de l'exploration: {e}")
        
        return None, None
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None, None

if __name__ == "__main__":
    dataset, table = test_phmev_tables()
    if dataset and table:
        print(f"\n🎯 Utiliser: dataset='{dataset}', table='{table}'")
    else:
        print(f"\n💡 Suggestion: Vérifier avec l'admin du projet BigQuery")
