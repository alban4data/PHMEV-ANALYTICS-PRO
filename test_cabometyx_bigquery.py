"""
Test pour vérifier la présence de Cabometyx dans BigQuery
"""

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os

# Configuration
project_id = 'test-db-473321'
dataset_id = 'dataset'
table_id = 'PHMEV2024'

# Initialisation du client BigQuery
try:
    # Chercher le fichier JSON dans le répertoire courant
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'test-db-473321-aed58eeb55a8.json')
    
    if os.path.exists(json_path):
        credentials = service_account.Credentials.from_service_account_file(json_path)
        client = bigquery.Client(credentials=credentials, project=project_id)
        print("🔗 Connexion BigQuery réussie avec fichier JSON local.")
    else:
        client = bigquery.Client(project=project_id)
        print("🔗 Connexion BigQuery réussie avec credentials par défaut.")
        
except Exception as e:
    print(f"❌ Erreur de connexion BigQuery: {e}")
    exit()

def test_cabometyx():
    print("🔍 Test de recherche Cabometyx...")
    
    # Test 1: Recherche dans L_ATC5 (colonne utilisée pour les médicaments)
    query1 = f"""
    SELECT DISTINCT L_ATC5
    FROM `{project_id}.{dataset_id}.{table_id}`
    WHERE LOWER(L_ATC5) LIKE '%cabome%'
    OR LOWER(L_ATC5) LIKE '%cabometyx%'
    LIMIT 10
    """
    
    print("📊 Recherche dans L_ATC5...")
    result1 = client.query(query1).to_dataframe()
    print(f"Résultats L_ATC5: {len(result1)} trouvés")
    if len(result1) > 0:
        print(result1['L_ATC5'].tolist())
    else:
        print("❌ Aucun résultat dans L_ATC5")
    
    # Test 2: Recherche dans l_cip13 (nom du médicament)
    query2 = f"""
    SELECT DISTINCT l_cip13
    FROM `{project_id}.{dataset_id}.{table_id}`
    WHERE LOWER(l_cip13) LIKE '%cabome%'
    OR LOWER(l_cip13) LIKE '%cabometyx%'
    LIMIT 10
    """
    
    print("\n📊 Recherche dans l_cip13...")
    result2 = client.query(query2).to_dataframe()
    print(f"Résultats l_cip13: {len(result2)} trouvés")
    if len(result2) > 0:
        print(result2['l_cip13'].tolist())
    else:
        print("❌ Aucun résultat dans l_cip13")
    
    # Test 3: Recherche générale dans toutes les colonnes texte
    query3 = f"""
    SELECT DISTINCT l_cip13, L_ATC5, atc1, l_atc1
    FROM `{project_id}.{dataset_id}.{table_id}`
    WHERE LOWER(l_cip13) LIKE '%cabome%'
    OR LOWER(L_ATC5) LIKE '%cabome%'
    OR LOWER(l_cip13) LIKE '%cabometyx%'
    OR LOWER(L_ATC5) LIKE '%cabometyx%'
    LIMIT 20
    """
    
    print("\n📊 Recherche générale...")
    result3 = client.query(query3).to_dataframe()
    print(f"Résultats généraux: {len(result3)} trouvés")
    if len(result3) > 0:
        print(result3.to_string())
    else:
        print("❌ Aucun résultat trouvé")
    
    # Test 4: Compter le nombre total de médicaments distincts
    query4 = f"""
    SELECT 
        COUNT(DISTINCT L_ATC5) as nb_L_ATC5,
        COUNT(DISTINCT l_cip13) as nb_l_cip13
    FROM `{project_id}.{dataset_id}.{table_id}`
    WHERE l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')
    AND l_cip13 IS NOT NULL
    """
    
    print("\n📊 Statistiques générales...")
    result4 = client.query(query4).to_dataframe()
    print(result4.to_string())
    
    # Test 5: Échantillon de médicaments pour voir le format
    query5 = f"""
    SELECT DISTINCT L_ATC5
    FROM `{project_id}.{dataset_id}.{table_id}`
    WHERE L_ATC5 IS NOT NULL 
    AND L_ATC5 != 'Non spécifié'
    AND L_ATC5 != ''
    ORDER BY L_ATC5
    LIMIT 20
    """
    
    print("\n📊 Échantillon de médicaments (L_ATC5)...")
    result5 = client.query(query5).to_dataframe()
    if len(result5) > 0:
        print(result5['L_ATC5'].tolist())

if __name__ == "__main__":
    test_cabometyx()
