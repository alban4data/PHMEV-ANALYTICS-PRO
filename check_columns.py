"""
🔍 Vérifier les vraies colonnes de PHMEV2024
"""

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

def check_columns():
    """Vérifier les colonnes disponibles"""
    
    PROJECT_ID = 'test-db-473321'
    
    try:
        credentials_path = "test-db-473321-aed58eeb55a8.json"
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
        
        # Requête pour voir toutes les colonnes
        query = """
        SELECT *
        FROM `test-db-473321.dataset.PHMEV2024`
        LIMIT 1
        """
        
        df = client.query(query).to_dataframe()
        
        print("📊 Colonnes disponibles dans PHMEV2024:")
        print("=" * 50)
        
        for i, col in enumerate(df.columns, 1):
            print(f"{i:2d}. {col}")
        
        print(f"\n📋 Total: {len(df.columns)} colonnes")
        
        # Chercher les colonnes ATC
        print(f"\n🧬 Colonnes ATC trouvées:")
        atc_cols = [col for col in df.columns if 'atc' in col.lower() or 'ATC' in col]
        for col in atc_cols:
            print(f"   - {col}")
        
        # Chercher les colonnes de libellés
        print(f"\n📝 Colonnes de libellés trouvées:")
        label_cols = [col for col in df.columns if col.startswith('l_') or col.startswith('L_')]
        for col in label_cols:
            print(f"   - {col}")
        
        return df.columns.tolist()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return []

if __name__ == "__main__":
    columns = check_columns()
