"""
Script pour intégrer le cache directement dans l'application
"""

import pickle
import json

def create_embedded_cache():
    """Crée un fichier Python avec le cache intégré"""
    
    try:
        # Charger le cache existant
        with open('filter_options_cache.pkl', 'rb') as f:
            cache_data = pickle.load(f)
        
        print(f"Cache chargé: {len(cache_data.get('medicaments', []))} médicaments")
        
        # Créer le fichier Python avec le cache intégré
        cache_code = f'''"""
Cache des options de filtres intégré pour Streamlit Cloud
Généré automatiquement - Ne pas modifier manuellement
"""

EMBEDDED_FILTER_CACHE = {repr(cache_data)}

def get_embedded_cache():
    """Retourne le cache intégré"""
    return EMBEDDED_FILTER_CACHE
'''
        
        with open('filter_cache_embedded.py', 'w', encoding='utf-8') as f:
            f.write(cache_code)
        
        print("✅ Cache intégré créé dans filter_cache_embedded.py")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    create_embedded_cache()
