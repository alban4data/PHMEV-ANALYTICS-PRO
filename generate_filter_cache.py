"""
🚀 Générateur de cache pour les options de filtres
Pré-calcule et stocke toutes les options pour un chargement ultra-rapide
"""

import json
import pickle
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

def generate_filter_cache():
    """Génère et sauvegarde le cache des options de filtres"""
    
    print("🚀 Génération du cache des options de filtres...")
    
    try:
        # Connexion BigQuery
        credentials = service_account.Credentials.from_service_account_file('test-db-473321-aed58eeb55a8.json')
        client = bigquery.Client(credentials=credentials, project='test-db-473321')
        
        print("✅ Connexion BigQuery établie")
        
        # Requête pour récupérer toutes les options
        query = """
        SELECT DISTINCT
            atc1, l_atc1,
            atc2, L_ATC2,
            atc3, L_ATC3,
            atc4, L_ATC4,
            ATC5, L_ATC5,
            COALESCE(NULLIF(nom_ville, ''), 'Non spécifiée') as ville,
            COALESCE(NULLIF(categorie_jur, ''), 'Non spécifiée') as categorie,
            COALESCE(NULLIF(nom_etb, ''), NULLIF(raison_sociale_etb, ''), 'Non spécifié') as etablissement,
            COALESCE(NULLIF(l_cip13, ''), 'Non spécifié') as medicament
        FROM `test-db-473321.dataset.PHMEV2024`
        WHERE l_cip13 NOT IN ('Non restitué', 'Non spécifié', 'Honoraires de dispensation')
        AND l_cip13 IS NOT NULL
        """
        
        print("📊 Exécution de la requête BigQuery...")
        df = client.query(query).to_dataframe()
        print(f"✅ {len(df)} lignes récupérées")
        
        # Construire les options
        print("🔧 Construction des options...")
        
        options = {}
        
        # ATC hiérarchiques
        if 'atc1' in df.columns:
            options['atc1'] = sorted([(row['atc1'], row['l_atc1']) for _, row in df[['atc1', 'l_atc1']].dropna().drop_duplicates().iterrows()])
            print(f"   ✅ ATC1: {len(options['atc1'])} options")
            
        if 'atc2' in df.columns:
            options['atc2'] = sorted([(row['atc2'], row['L_ATC2']) for _, row in df[['atc2', 'L_ATC2']].dropna().drop_duplicates().iterrows()])
            print(f"   ✅ ATC2: {len(options['atc2'])} options")
            
        if 'atc3' in df.columns:
            options['atc3'] = sorted([(row['atc3'], row['L_ATC3']) for _, row in df[['atc3', 'L_ATC3']].dropna().drop_duplicates().iterrows()])
            print(f"   ✅ ATC3: {len(options['atc3'])} options")
            
        if 'atc4' in df.columns:
            options['atc4'] = sorted([(row['atc4'], row['L_ATC4']) for _, row in df[['atc4', 'L_ATC4']].dropna().drop_duplicates().iterrows()])
            print(f"   ✅ ATC4: {len(options['atc4'])} options")
            
        if 'ATC5' in df.columns:
            options['atc5'] = sorted([(row['ATC5'], row['L_ATC5']) for _, row in df[['ATC5', 'L_ATC5']].dropna().drop_duplicates().iterrows()])
            print(f"   ✅ ATC5: {len(options['atc5'])} options")
        
        # Autres options
        options['villes'] = sorted(df['ville'].dropna().unique().tolist())
        print(f"   ✅ Villes: {len(options['villes'])} options")
        
        options['categories'] = sorted(df['categorie'].dropna().unique().tolist())
        print(f"   ✅ Catégories: {len(options['categories'])} options")
        
        options['etablissements'] = sorted(df['etablissement'].dropna().unique().tolist())
        print(f"   ✅ Établissements: {len(options['etablissements'])} options")
        
        options['medicaments'] = sorted(df['medicament'].dropna().unique().tolist())
        print(f"   ✅ Médicaments: {len(options['medicaments'])} options")
        
        # Ajouter métadonnées
        options['_metadata'] = {
            'generated_at': datetime.now().isoformat(),
            'total_records': len(df),
            'version': '1.0'
        }
        
        # Sauvegarder en JSON (lisible)
        with open('filter_options_cache.json', 'w', encoding='utf-8') as f:
            json.dump(options, f, ensure_ascii=False, indent=2)
        print("✅ Cache JSON sauvegardé")
        
        # Sauvegarder en pickle (plus rapide à charger)
        with open('filter_options_cache.pkl', 'wb') as f:
            pickle.dump(options, f)
        print("✅ Cache pickle sauvegardé")
        
        # Statistiques
        print("\n📊 Statistiques du cache généré:")
        print(f"   🧬 ATC1: {len(options.get('atc1', []))} options")
        print(f"   🧬 ATC2: {len(options.get('atc2', []))} options") 
        print(f"   🧬 ATC3: {len(options.get('atc3', []))} options")
        print(f"   🧬 ATC4: {len(options.get('atc4', []))} options")
        print(f"   🧬 ATC5: {len(options.get('atc5', []))} options")
        print(f"   🏙️ Villes: {len(options['villes'])} options")
        print(f"   🏥 Catégories: {len(options['categories'])} options")
        print(f"   🏢 Établissements: {len(options['etablissements'])} options")
        print(f"   💊 Médicaments: {len(options['medicaments'])} options")
        
        # Vérifier si Cabometyx est présent
        cabometyx_found = [med for med in options['medicaments'] if 'cabometyx' in med.lower()]
        if cabometyx_found:
            print(f"\n✅ Cabometyx trouvé: {cabometyx_found}")
        else:
            print("\n❌ Cabometyx non trouvé dans le cache")
        
        print(f"\n🎉 Cache généré avec succès à {options['_metadata']['generated_at']}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du cache: {e}")
        return False

if __name__ == "__main__":
    success = generate_filter_cache()
    if success:
        print("\n🚀 Le cache est prêt ! L'application sera maintenant ultra-rapide au démarrage.")
    else:
        print("\n💥 Échec de la génération du cache.")
