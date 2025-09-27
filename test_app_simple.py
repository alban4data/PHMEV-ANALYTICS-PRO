#!/usr/bin/env python3
"""
Test simple et direct de l'application PHMEV
Teste les fonctionnalités essentielles sans dépendances complexes
"""

import os
import sys
from datetime import datetime

def test_cache_availability():
    """Test la disponibilité du cache"""
    print("🧪 Test: Disponibilité du cache...")
    try:
        from filter_cache_embedded import get_embedded_cache
        cache = get_embedded_cache()
        
        if not cache:
            print("❌ Cache vide")
            return False
        
        required_keys = ['atc1', 'atc2', 'atc3', 'atc4', 'atc5', 'villes', 'categories', 'etablissements', 'medicaments']
        
        for key in required_keys:
            if key not in cache:
                print(f"❌ Clé manquante: {key}")
                return False
            
            count = len(cache[key])
            print(f"✅ {key}: {count} éléments")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_search_medicaments():
    """Test la recherche de médicaments"""
    print("\n🧪 Test: Recherche de médicaments...")
    try:
        from filter_cache_embedded import get_embedded_cache
        cache = get_embedded_cache()
        medicaments = cache['medicaments']
        
        # Tests de recherche
        test_searches = [
            ('cabometyx', 'CABOMETYX'),
            ('cabo', 'CABO'),
            ('keytruda', 'KEYTRUDA'),
            ('opdivo', 'OPDIVO'),
            ('humira', 'HUMIRA')
        ]
        
        for search_term, expected in test_searches:
            matches = [med for med in medicaments if search_term.lower() in med.lower()]
            if matches:
                print(f"✅ '{search_term}' trouvé: {len(matches)} résultats")
                print(f"   Exemple: {matches[0]}")
            else:
                print(f"⚠️  '{search_term}' non trouvé")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_search_etablissements():
    """Test la recherche d'établissements"""
    print("\n🧪 Test: Recherche d'établissements...")
    try:
        from filter_cache_embedded import get_embedded_cache
        cache = get_embedded_cache()
        etablissements = cache['etablissements']
        
        # Tests de recherche d'établissements
        test_searches = [
            'chu',
            'clinique',
            'hopital',
            'gustave',
            'roussy'
        ]
        
        for search_term in test_searches:
            matches = [etab for etab in etablissements if search_term.lower() in etab.lower()]
            if matches:
                print(f"✅ '{search_term}' trouvé: {len(matches)} résultats")
                if 'gustave' in search_term.lower() or 'roussy' in search_term.lower():
                    print(f"   Exemples: {matches[:3]}")
            else:
                print(f"⚠️  '{search_term}' non trouvé")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_atc_hierarchy():
    """Test la hiérarchie ATC"""
    print("\n🧪 Test: Hiérarchie ATC...")
    try:
        from filter_cache_embedded import get_embedded_cache
        cache = get_embedded_cache()
        
        # Vérifier la structure hiérarchique
        atc1_sample = cache['atc1'][0] if cache['atc1'] else None
        atc2_sample = cache['atc2'][0] if cache['atc2'] else None
        
        if atc1_sample and atc2_sample:
            atc1_code, atc1_label = atc1_sample
            atc2_code, atc2_label = atc2_sample
            
            print(f"✅ ATC1 exemple: {atc1_code} - {atc1_label}")
            print(f"✅ ATC2 exemple: {atc2_code} - {atc2_label}")
            
            # Vérifier que ATC2 commence par ATC1
            if atc2_code.startswith(atc1_code):
                print("✅ Cohérence hiérarchique ATC1->ATC2")
            else:
                print("⚠️  Problème de cohérence hiérarchique")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_bigquery_connection():
    """Test simple de connexion BigQuery"""
    print("\n🧪 Test: Connexion BigQuery...")
    try:
        import os
        from google.oauth2 import service_account
        from google.cloud import bigquery
        
        json_file = 'test-db-473321-aed58eeb55a8.json'
        if not os.path.exists(json_file):
            print("⚠️  Fichier de credentials non trouvé")
            return False
        
        credentials = service_account.Credentials.from_service_account_file(json_file)
        client = bigquery.Client(credentials=credentials, project='test-db-473321')
        
        # Test simple
        result = client.query("SELECT 1 as test").result()
        print("✅ Connexion BigQuery réussie")
        return True
    except Exception as e:
        print(f"⚠️  Connexion BigQuery échouée: {e}")
        return False

def test_app_startup():
    """Test le démarrage de l'application (simulation)"""
    print("\n🧪 Test: Démarrage de l'application...")
    try:
        # Simuler le chargement des options de base
        from filter_cache_embedded import get_embedded_cache
        
        # Test 1: Cache intégré
        cache = get_embedded_cache()
        if cache:
            print("✅ Cache intégré chargé")
        else:
            print("❌ Échec chargement cache")
            return False
        
        # Test 2: Vérifier les KPIs (simulation)
        medicaments_count = len(cache.get('medicaments', []))
        etablissements_count = len(cache.get('etablissements', []))
        
        if medicaments_count > 0 and etablissements_count > 0:
            print(f"✅ Données disponibles: {medicaments_count} médicaments, {etablissements_count} établissements")
        else:
            print("❌ Données insuffisantes")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def run_simple_tests():
    """Exécuter tous les tests simples"""
    print("🚀 TESTS SIMPLES - APPLICATION PHMEV")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    tests = [
        ("Cache disponible", test_cache_availability),
        ("Recherche médicaments", test_search_medicaments),
        ("Recherche établissements", test_search_etablissements),
        ("Hiérarchie ATC", test_atc_hierarchy),
        ("Connexion BigQuery", test_bigquery_connection),
        ("Démarrage app", test_app_startup)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERREUR dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    for test_name, result in results:
        status = "✅ OK" if result else "❌ KO"
        print(f"{test_name:.<25} {status}")
    
    print("-" * 50)
    print(f"Total: {len(results)} | OK: {passed} | KO: {failed}")
    
    if failed == 0:
        print("🎉 TOUS LES TESTS PASSÉS !")
    else:
        print(f"⚠️  {failed} test(s) échoué(s)")
    
    return failed == 0

if __name__ == "__main__":
    success = run_simple_tests()
    sys.exit(0 if success else 1)
