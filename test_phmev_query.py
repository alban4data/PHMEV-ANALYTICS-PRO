"""
🧪 Test de requête sur la vraie table PHMEV2024
"""

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

def test_phmev_query():
    """Test une vraie requête sur PHMEV2024"""
    
    print("🧪 Test de requête sur PHMEV2024...")
    
    PROJECT_ID = 'test-db-473321'
    DATASET_ID = 'dataset'
    TABLE_ID = 'PHMEV2024'
    
    try:
        # Initialiser le client BigQuery
        credentials_path = "test-db-473321-aed58eeb55a8.json"
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
        
        print(f"✅ Connexion réussie au projet: {PROJECT_ID}")
        
        # Test 1: Structure de la table
        print("\n📋 Test 1: Structure de la table")
        structure_query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        LIMIT 3
        """
        
        df_sample = client.query(structure_query).to_dataframe()
        print(f"✅ Échantillon récupéré: {len(df_sample)} lignes, {len(df_sample.columns)} colonnes")
        
        print(f"\n📊 Colonnes disponibles ({len(df_sample.columns)}):")
        for i, col in enumerate(df_sample.columns):
            if i < 15:  # Afficher les 15 premières
                print(f"   {i+1:2d}. {col}")
            elif i == 15:
                print(f"   ... et {len(df_sample.columns) - 15} autres colonnes")
                break
        
        # Test 2: Recherche de Cabometyx
        print(f"\n🔍 Test 2: Recherche de Cabometyx")
        cabometyx_query = f"""
        SELECT 
            L_ATC5,
            nom_etb,
            nom_ville,
            REM,
            BSE,
            BOITES
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE LOWER(L_ATC5) LIKE '%cabometyx%' 
        OR LOWER(L_ATC5) LIKE '%cabozantinib%'
        LIMIT 10
        """
        
        df_cabometyx = client.query(cabometyx_query).to_dataframe()
        print(f"✅ Cabometyx trouvé: {len(df_cabometyx)} lignes")
        
        if len(df_cabometyx) > 0:
            print("\n📊 Aperçu Cabometyx:")
            print(df_cabometyx[['L_ATC5', 'nom_etb', 'REM', 'BOITES']].head())
        
        # Test 3: Statistiques générales
        print(f"\n📈 Test 3: Statistiques générales")
        stats_query = f"""
        SELECT 
            COUNT(*) as total_lignes,
            COUNT(DISTINCT nom_etb) as etablissements_uniques,
            COUNT(DISTINCT L_ATC5) as medicaments_uniques,
            COUNT(DISTINCT nom_ville) as villes_uniques,
            SUM(REM) as remboursement_total,
            SUM(BOITES) as boites_totales,
            AVG(REM) as remboursement_moyen
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')
        AND l_cip13 IS NOT NULL
        """
        
        df_stats = client.query(stats_query).to_dataframe()
        
        if len(df_stats) > 0:
            stats = df_stats.iloc[0]
            print(f"✅ Statistiques calculées:")
            print(f"   📊 Lignes totales: {stats['total_lignes']:,}")
            print(f"   🏥 Établissements uniques: {stats['etablissements_uniques']:,}")
            print(f"   💊 Médicaments uniques: {stats['medicaments_uniques']:,}")
            print(f"   🏙️ Villes uniques: {stats['villes_uniques']:,}")
            print(f"   💰 Remboursement total: {stats['remboursement_total']:,.2f}€")
            print(f"   📦 Boîtes totales: {stats['boites_totales']:,}")
            print(f"   💵 Remboursement moyen: {stats['remboursement_moyen']:,.2f}€")
        
        # Test 4: Top 5 établissements
        print(f"\n🏥 Test 4: Top 5 établissements")
        top_etabs_query = f"""
        SELECT 
            COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié') as etablissement,
            nom_ville as ville,
            SUM(REM) as total_remboursement,
            SUM(BOITES) as total_boites,
            COUNT(*) as nb_lignes
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')
        AND l_cip13 IS NOT NULL
        GROUP BY etablissement, ville
        ORDER BY total_remboursement DESC
        LIMIT 5
        """
        
        df_top_etabs = client.query(top_etabs_query).to_dataframe()
        print(f"✅ Top établissements récupéré:")
        print(df_top_etabs[['etablissement', 'ville', 'total_remboursement', 'total_boites']])
        
        print(f"\n🎉 Tous les tests réussis ! BigQuery est opérationnel !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print(f"🔍 Type d'erreur: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_phmev_query()
    if success:
        print(f"\n✅ BigQuery est prêt pour l'application Streamlit !")
    else:
        print(f"\n❌ Problème avec BigQuery, utiliser le mode démo")
